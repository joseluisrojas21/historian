<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import 'chartjs-adapter-date-fns';

  let chart: Chart | null = null;
  let temperatureData: { timestamp: string, temperature: number }[] = [];
  let timeLabels: string[] = [];
  let canvas: HTMLCanvasElement | null = null;

  // Slider values representing the range of data to display
  let sliderMin = 0;
  let sliderMax = 100;

  // Fetch temperature data
  async function fetchTemperatureData() {
    try {
      const response = await fetch('http://localhost:3000/temperature');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      // Sort and store data
      temperatureData = data.sort((a: { timestamp: string }, b: { timestamp: string }) => 
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );

      updateChart();
    } catch (error) {
      console.error('Error fetching temperature data:', error);
    }
  }

  // Filter data based on slider range and update the chart
  function updateChart() {
    const dataCount = temperatureData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = temperatureData.slice(minIndex, maxIndex + 1);

    timeLabels = filteredData.map((item) => item.timestamp);
    const temperatures = filteredData.map((item) => item.temperature);

    if (chart) {
      chart.data.labels = timeLabels;
      chart.data.datasets[0].data = temperatures;
      chart.update();
    } else if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'Temperature over Time',
              data: temperatures,
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
                  unit: 'minute'
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

  onMount(() => {
    fetchTemperatureData();
    const interval = setInterval(fetchTemperatureData, 10000); // Update every 10 seconds

    onDestroy(() => {
      clearInterval(interval);
    });
  });
</script>

<main>
  <h1>Temperature Data Chart</h1>
  <canvas bind:this={canvas} width="400" height="200"></canvas>

  <div class="slider-controls">
    <label>
      Start Range:
      <input type="range" min="0" max="100" bind:value={sliderMin} on:change={updateChart} />
    </label>
    <label>
      End Range:
      <input type="range" min="0" max="100" bind:value={sliderMax} on:change={updateChart} />
    </label>
  </div>
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

  .slider-controls {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
    gap: 1rem;
  }

  label {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input[type="range"] {
    width: 150px;
  }
</style>
