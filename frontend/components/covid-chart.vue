<template>
  <svg
    id="chart"
    width="600"
    height="400"
    viewBox="0 0 600 400"
    perserveAspectRatio="xMinYMid"
  ></svg>
</template>

<script>
import * as d3 from 'd3'
export default {
  data() {
    return {
      currentWidth: 0,
      currentHeight: 0,
    }
  },
  mounted() {
    // initialize the chart
    const chart = d3.select('#chart')
    this.resizeChart(chart)
    window.addEventListener(
      'resize',
      function () {
        this.resizeChart(chart)
      }.bind(this)
    )

    // generate the intial dataset
    const data = this.generateDataset()
    const nodes = data.map((d) => Object.create(d))
    const simulation = this.setupCollision(data)

    // create the chart and append the initial dots
    const svg = chart
      .call(
        d3
          .zoom()
          .scaleExtent([1, 1])
          .on('zoom', function (event) {
            svg.attr('transform', event.transform)
          })
      )
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 4)
      .attr('x', (d, i) => d.x)
      .attr('y', (d, i) => d.y)
      .attr('fill', '#000000')

    // update the x and y deltas each tick (for collisions)
    simulation.on('tick', () => {
      svg.attr('cx', (d) => d.x).attr('cy', (d) => d.y)
    })
  },
  methods: {
    generateDataset() {
      const data = []
      for (let i = 0; i < 500; i++) {
        data[i] = {
          x: Math.floor(Math.random() * this.currentWidth),
          y: Math.random() * this.currentHeight,
        }
      }
      return data
    },
    setupCollision(data) {
      return d3
        .forceSimulation(data)
        .force('charge', d3.forceManyBody())
        .force(
          'center',
          d3.forceCenter(this.currentWidth / 2, this.currentHeight / 2)
        )
    },
    resizeChart(chart) {
      const container = chart.node().parentNode
      this.currentWidth = container.getBoundingClientRect().width
      this.currentHeight = container.getBoundingClientRect().height
      chart.attr('width', this.currentWidth)
      chart.attr('height', this.currentHeight)
    },
  },
}
</script>

<style>
#chart {
  background-color: white;
}
</style>
