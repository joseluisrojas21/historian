<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import 'chartjs-adapter-date-fns';

  // Charts
  let temperatureChart: Chart | null = null;
  let pressureChart:    Chart | null = null;
  let irradianceChart:  Chart | null = null;
  let humidityChart:    Chart | null = null;
  let garageChart:      Chart | null = null;
  let bathroomChart:    Chart | null = null;
  let bedroomChart:     Chart | null = null;
  let lrChart:          Chart | null = null;

  // Data
  let irradianceData:  { timestamp: string, irradiance: number }[] = [];
  let temperatureData: { timestamp: string, temperature: number }[] = [];
  let pressureData:    { timestamp: string, pressure: number }[] = [];
  let humidityData:    { timestamp: string, humidity: number }[] = [];
  let garageData:      { timestamp: string, garage: number }[] = [];
  let bathroomData:    { timestamp: string, bathroom: number }[] = [];
  let bedroomData:     { timestamp: string, bedroom: number }[] = [];
  let lrData:          { timestamp: string, lr: number }[] = [];

  // Time labels
  let timeLabels: string[] = [];

  // Canvas
  let tempCanvas:           HTMLCanvasElement | null = null;
  let pressureCanvas:       HTMLCanvasElement | null = null;
  let irradianceCanvas:     HTMLCanvasElement | null = null;
  let humidityCanvas:       HTMLCanvasElement | null = null;
  let motionGarageCanvas:   HTMLCanvasElement | null = null;
  let motionBathroomCanvas: HTMLCanvasElement | null = null;
  let motionBedroomCanvas:  HTMLCanvasElement | null = null;
  let motionLRCanvas:       HTMLCanvasElement | null = null;

  // Slider values representing the range of data to display
  let sliderMin = 0;
  let sliderMax = 100;

  function sortByTimestamp(data: any[]) {
    return data.sort(( a: { timestamp: string | number | Date; }, b: { timestamp: string | number | Date; }) =>
    new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
  }

  // Fetch all data
  async function fetchAllData() {
    try {
      const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/allData`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      // Assigning data to each chart variable
      temperatureData = sortByTimestamp(data.temperatureData);
      pressureData = sortByTimestamp(data.pressureData);
      irradianceData = sortByTimestamp(data.irradianceData);
      humidityData = sortByTimestamp(data.humidityData);
      garageData = sortByTimestamp(data.garageData);
      bathroomData = sortByTimestamp(data.bathroomData);
      bedroomData = sortByTimestamp(data.bedroomData);
      lrData = sortByTimestamp(data.lrData);

      // Update charts
      updateCharts();

    } catch (error) {
      console.error('Error fetching all data:', error);
    }
  }

  function updateCharts() {
    updateTemperatureChart();
    updatePressureChart();
    updateIrradianceChart();
    updateHumidityChart();
    updateGarageChart();
    updateBathroomChart();
    updateBedroomChart();
    updateLRChart();
  }

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
                beginAtZero: false,
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
                beginAtZero: false,
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
                beginAtZero: false,
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

  function updateHumidityChart() {
    const dataCount = humidityData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = humidityData.slice(minIndex, maxIndex + 1);

    const humidityLevels = filteredData.map((item) => item.humidity);

    if (humidityChart) {
      humidityChart.data.labels = timeLabels;
      humidityChart.data.datasets[0].data = humidityLevels;
      humidityChart.update();
    } else if (humidityCanvas) {
      const ctx = humidityCanvas.getContext('2d');
      if (ctx) {
        humidityChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'Humidity over Time',
              data: humidityLevels,
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
                beginAtZero: false,
                title: {
                  display: true,
                  text: 'Humidity %'
                }
              }
            }
          }
        });
      }
    }
  }

  function updateGarageChart() {
    const dataCount = garageData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = garageData.slice(minIndex, maxIndex + 1);

    const garageLevels = filteredData.map((item) => item.garage);

    if (garageChart) {
      garageChart.data.labels = timeLabels;
      garageChart.data.datasets[0].data = garageLevels;
      garageChart.update();
    } else if (motionGarageCanvas) {
      const ctx = motionGarageCanvas.getContext('2d');
      if (ctx) {
        garageChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'Garage movement over Time',
              data: garageLevels,
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
                beginAtZero: false,
                title: {
                  display: true,
                  text: 'Motion'
                }
              }
            }
          }
        });
      }
    }
  }

  function updateBathroomChart() {
    const dataCount = bathroomData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = bathroomData.slice(minIndex, maxIndex + 1);

    const bathroomLevels = filteredData.map((item) => item.bathroom);

    if (bathroomChart) {
      bathroomChart.data.labels = timeLabels;
      bathroomChart.data.datasets[0].data = bathroomLevels;
      bathroomChart.update();
    } else if (motionBathroomCanvas) {
      const ctx = motionBathroomCanvas.getContext('2d');
      if (ctx) {
        bathroomChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'Bathroom over Time',
              data: bathroomLevels,
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
                beginAtZero: false,
                title: {
                  display: true,
                  text: 'Motion'
                }
              }
            }
          }
        });
      }
    }
  }

  function updateBedroomChart() {
    const dataCount = bedroomData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = bedroomData.slice(minIndex, maxIndex + 1);

    const bedroomLevels = filteredData.map((item) => item.bedroom);

    if (bedroomChart) {
      bedroomChart.data.labels = timeLabels;
      bedroomChart.data.datasets[0].data = bedroomLevels;
      bedroomChart.update();
    } else if (motionBedroomCanvas) {
      const ctx = motionBedroomCanvas.getContext('2d');
      if (ctx) {
        bedroomChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'Bathroom over Time',
              data: bedroomLevels,
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
                beginAtZero: false,
                title: {
                  display: true,
                  text: 'Motion'
                }
              }
            }
          }
        });
      }
    }
  }

  function updateLRChart() {
    const dataCount = lrData.length;
    const minIndex = Math.floor((sliderMin / 100) * dataCount);
    const maxIndex = Math.floor((sliderMax / 100) * dataCount);
    const filteredData = lrData.slice(minIndex, maxIndex + 1);

    const lrLevels = filteredData.map((item) => item.lr);

    if (lrChart) {
      lrChart.data.labels = timeLabels;
      lrChart.data.datasets[0].data = lrLevels;
      lrChart.update();
    } else if (motionLRCanvas) {
      const ctx = motionLRCanvas.getContext('2d');
      if (ctx) {
        lrChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: timeLabels,
            datasets: [{
              label: 'LR over Time',
              data: lrLevels,
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
                beginAtZero: false,
                title: {
                  display: true,
                  text: 'Motion'
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
    fetchAllData();
    const interval = setInterval(() => {
      fetchAllData();
    }, 10000); // Update every 10 seconds

    onDestroy(() => {
      clearInterval(interval);
    });
  });
</script>

<main>
  <!-- <h1>Historian</h1> -->
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

    <div class="chart">
      <h2>Humidity Data</h2>
      <canvas bind:this={humidityCanvas} width="300" height="150"></canvas>
    </div>
  </div>

  <div class="charts-container">
    <div class="chart">
      <h2>Garage Data</h2>
      <canvas bind:this={motionGarageCanvas} width="300" height="150"></canvas>
    </div>

    <div class="chart">
      <h2>Bathroom Data</h2>
      <canvas bind:this={motionBathroomCanvas} width="300" height="150"></canvas>
    </div>
  </div>

  <div class="charts-container">
    <div class="chart">
      <h2>Bedroom Data</h2>
      <canvas bind:this={motionBedroomCanvas} width="300" height="150"></canvas>
    </div>

    <div class="chart">
      <h2>LR Data</h2>
      <canvas bind:this={motionLRCanvas} width="300" height="150"></canvas>
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
        on:change={() => { updateCharts(); }}
      />
    </label>
    <label>
      End Range:
      <input 
        type="range" 
        min="0" 
        max="100" 
        bind:value={sliderMax} 
        on:change={() => { updateCharts(); }}
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
