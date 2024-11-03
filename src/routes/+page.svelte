<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  let chart: Chart | null = null;
  let temperatureData: number[] = [];
  let timeLabels: string[] = [];
  let canvas: HTMLCanvasElement | null = null;

  async function fetchTemperatureData() {
    try {
      const response = await fetch('http://localhost:3000/temperature');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      // Sort and extract data
      const sortedData = data.sort((a: { timestamp: string }, b: { timestamp: string }) => {
        return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
      });
      timeLabels = sortedData.map((item: { timestamp: string }) => item.timestamp);
      temperatureData = sortedData.map((item: { temperature: number }) => item.temperature);

      // Update the chart
      if (chart) {
        chart.data.labels = timeLabels;
        chart.data.datasets[0].data = temperatureData;
        chart.update(); // Redraw the chart with new data
      } else {
        if (canvas) {
          const ctx = canvas.getContext('2d');
          if (ctx) {
            chart = new Chart(ctx, {
              type: 'line',
              data: {
                labels: timeLabels,
                datasets: [{
                  label: 'Temperature over Time',
                  data: temperatureData,
                  borderColor: 'rgba(75, 192, 192, 1)',
                  fill: false,
                  tension: 0.1
                }]
              },
              options: {
                scales: {
                  x: {
                    type: 'time',
                    time: {
                      unit: 'minute' // Change unit as needed
                    },
                    title: {
                      display: true,
                      text: 'Time'
                    }
                  },
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Temperature (°C)'
                    }
                  }
                }
              }
            });
          }
        }
      }
    } catch (error) {
      console.error('Error fetching temperature data:', error);
    }
  }

  onMount(() => {
    fetchTemperatureData();
    const interval = setInterval(fetchTemperatureData, 10000); // Update every 10 seconds

    // Cleanup interval on component destroy
    onDestroy(() => {
      clearInterval(interval);
    });
  });
</script>

<main>
  <h1>Temperature Data Chart</h1>
  <canvas bind:this={canvas} width="400" height="200"></canvas>
</main>

<style>
  main {
    font-family: Arial, sans-serif;
    text-align: center;
    padding: 2rem;
  }

  h1 {
    color: #333;
  }

  canvas {
    margin-top: 1rem;
    border: 1px solid #ccc;
  }
</style>
