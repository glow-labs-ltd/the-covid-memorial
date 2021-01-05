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
      container: null,
      currentWidth: 0,
      currentHeight: 0,
      numDots: 500,
      dotColours: [
        '#73446A',
        '#F4C50F',
        '#45036E',
        '#1E447A',
        '#000000',
        '#D57004',
        '#2D5D2E',
      ],
    }
  },
  mounted() {
    // initialize the chart
    const chart = d3.select('#chart')
    this.container = chart.node().parentNode
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
    const boxG = chart
      .call(
        d3
          .zoom()
          .scaleExtent([0.01, 1])
          .on(
            'zoom',
            function (event) {
              const transform = event.transform
              const scale = transform.k
              const dx = transform.x % (this.currentHeight * scale)
              const dy = transform.y % (this.currentWidth * scale)
              svg.attr(
                'transform',
                'translate(' + dx + ',' + dy + ')scale(' + scale + ')'
              )
              boxG.attr(
                'transform',
                'translate(' + dx + ',' + dy + ')scale(' + scale + ')'
              )
            }.bind(this)
          )
      )
      .append('g')

    const svg = chart
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 12)
      .attr('x', (d, i) => d.x)
      .attr('y', (d, i) => d.y)
      .attr('fill', (d, i) => d.colour)

    // update the x and y deltas each tick (for collisions)
    simulation.on('tick', () => {
      svg.attr('cx', (d) => d.x).attr('cy', (d) => d.y)
    })
  },
  methods: {
    generateDataset() {
      const data = []
      for (let i = 0; i < this.numDots; i++) {
        data[i] = {
          x: Math.floor(Math.random() * this.currentWidth),
          y: Math.floor(Math.random() * this.currentHeight),
          colour: this.dotColours[
            Math.floor(Math.random() * this.dotColours.length)
          ],
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
      this.currentWidth = this.container.getBoundingClientRect().width
      this.currentHeight = this.container.getBoundingClientRect().height
      chart.attr('width', this.currentWidth)
      chart.attr('height', this.currentHeight)
    },
  },
}
</script>

<style>
#chart {
  background-color: #f5f6f5;
}
</style>
