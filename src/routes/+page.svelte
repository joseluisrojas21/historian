<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import 'chartjs-adapter-date-fns';

  let temperatureChart: Chart | null = null;
  let pressureChart: Chart | null = null;
  let irradianceChart: Chart | null = null;
  let irradianceData: { timestamp: string, irradiance: number }[] = [];
  let temperatureData: { timestamp: string, temperature: number }[] = [];
  let pressureData: { timestamp: string, pressure: number }[] = [];
  let timeLabels: string[] = [];
  let tempCanvas: HTMLCanvasElement | null = null; // Canvas for temperature chart
  let pressureCanvas: HTMLCanvasElement | null = null; // Canvas for pressure chart
  let irradianceCanvas: HTMLCanvasElement | null = null; // Canvas for irradiance chart

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
      
      // Sort and store temperature data
      temperatureData = data.sort((a: { timestamp: string }, b: { timestamp: string }) => 
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );

      updateTemperatureChart();
    } catch (error) {
      console.error('Error fetching temperature data:', error);
    }
  }

  // Fetch pressure data
  async function fetchPressureData() {
    try {
      const response = await fetch('http://localhost:3000/pressure');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      
      // Sort and store pressure data
      pressureData = data.sort((a: { timestamp: string }, b: { timestamp: string }) => 
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );

      updatePressureChart();
    } catch (error) {
      console.error('Error fetching pressure data:', error);
    }
  }

  async function fetchIrradianceData() {
    try {
      const response = await fetch('http://localhost:3000/irradiance');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log(data);
      // Sort and store temperature data
      irradianceData = data.sort((a: { timestamp: string }, b: { timestamp: string }) => 
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );

      updateIrradianceChart();
    } catch (error) {
      console.error('Error fetching temperature data:', error);
    }
  }

  // Filter data based on slider range and update the temperature chart
  function updateTemperatureChart() {
    const dataCount = temperatureData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = temperatureData.slice(minIndex, maxIndex + 1);

    timeLabels = filteredData.map((item) => item.timestamp);
    const temperatures = filteredData.map((item) => item.temperature);

    if (temperatureChart) {
      temperatureChart.data.labels = timeLabels;
      temperatureChart.data.datasets[0].data = temperatures;
      temperatureChart.update();
    } else if (tempCanvas) {
      const ctx = tempCanvas.getContext('2d');
      if (ctx) {
        temperatureChart = new Chart(ctx, {
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

  // Filter data based on slider range and update the pressure chart
  function updatePressureChart() {
    const dataCount = pressureData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = pressureData.slice(minIndex, maxIndex + 1);

    const pressures = filteredData.map((item) => item.pressure);

    if (pressureChart) {
      pressureChart.data.labels = timeLabels; // Use the same time labels
      pressureChart.data.datasets[0].data = pressures;
      pressureChart.update();
    } else if (pressureCanvas) {
      const ctx = pressureCanvas.getContext('2d');
      if (ctx) {
        pressureChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'Pressure over Time',
              data: pressures,
              borderColor: 'rgba(255, 99, 132, 1)',
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
                  text: 'Pressure (hPa)'
                }
              }
            }
          }
        });
      }
    }
  }

  // Filter data based on slider range and update the solar chart
  function updateIrradianceChart() {
    const dataCount = irradianceData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = irradianceData.slice(minIndex, maxIndex + 1);

    const radiationLevels = filteredData.map((item) => item.irradiance);

    if (irradianceChart) {
      irradianceChart.data.labels = timeLabels;
      irradianceChart.data.datasets[0].data = radiationLevels;
      irradianceChart.update();
    } else if (irradianceCanvas) {
      const ctx = irradianceCanvas.getContext('2d');
      if (ctx) {
        irradianceChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'Solar Radiation over Time',
              data: radiationLevels,
              borderColor: 'rgba(255, 206, 86, 1)',
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
                  text: 'Radiation (W/m²)'
                }
              }
            }
          }
        });
      }
    }
  }

  onMount(() => {
    document.title = "Historian";
    fetchTemperatureData();
    fetchPressureData();
    fetchIrradianceData();
    const interval = setInterval(() => {
      fetchTemperatureData();
      fetchPressureData();
      fetchIrradianceData();
    }, 10000); // Update every 10 seconds

    onDestroy(() => {
      clearInterval(interval);
    });
  });
</script>

<main>
  <h1>Historian</h1>
  
  <div class="charts-container">
    <div class="chart">
      <h2>Temperature Data</h2>
      <canvas bind:this={tempCanvas} width="300" height="150"></canvas>
    </div>
    
    <div class="chart">
      <h2>Pressure Data</h2>
      <canvas bind:this={pressureCanvas} width="300" height="150"></canvas>
    </div>
  </div>

  <div class="charts-container">
    <div class="chart">
      <h2>Irradiance Data</h2>
      <canvas bind:this={irradianceCanvas} width="300" height="150"></canvas>
    </div>
  </div>

  <div class="slider-controls">
    <label>
      Start Range:
      <input 
        type="range" 
        min="0" 
        max="100" 
        bind:value={sliderMin} 
        on:change={() => { updateTemperatureChart(); updatePressureChart(); updateIrradianceChart(); }} 
      />
    </label>
    <label>
      End Range:
      <input 
        type="range" 
        min="0" 
        max="100" 
        bind:value={sliderMax} 
        on:change={() => { updateTemperatureChart(); updatePressureChart(); updateIrradianceChart(); }} 
      />
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

  h2 {
    color: #555;
  }

  .charts-container {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 2rem;
  }

  .chart {
    width: 45%;
    text-align: center;
  }

  canvas {
    border: 1px solid #ccc;
  }

  .slider-controls {
    margin-top: 2rem;
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
