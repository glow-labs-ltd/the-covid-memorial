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
      numDots: 600,
      dotBlur: 7,
      maxBgDotRadius: 16,
      minBgDotRadius: 6,
    }
  },
  mounted() {
    // initialize the chart
    const chart = this.initializeChart()

    // create the background dots
    const bG = chart.append('g')
    const data = this.generateDataset(
      this.currentWidth * 2,
      this.currentHeight * 2,
      this.minBgDotRadius,
      this.maxBgDotRadius,
      this.numDots
    )
    const nodes = data.map((d) => Object.create(d))
    const simulation = this.setupCollision(data)
    const bDots = bG
      .append('g')
      .attr('filter', 'url(#blur)')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', (d, i) => d.radius)
      .attr('cx', (d, i) => d.x)
      .attr('cy', (d, i) => d.y)
      .attr('fill', '#000000')
      .style('opacity', 0.6)
    simulation.on('tick', () => {
      bDots.attr('cx', (d) => d.x).attr('cy', (d) => d.y)
    })

    // create the foreground layer
    const fG = chart.append('g')
    const fData = this.generateDataset(
      this.currentWidth * 2,
      this.currentHeight * 2,
      14,
      14,
      this.numDots / 4
    )
    const fNodes = fData.map((d) => Object.create(d))
    const fSimulation = this.setupCollision(fData)
    const fDots = fG
      .append('g')
      .attr('width', this.currentWidth)
      .attr('height', this.currentHeight)
      .selectAll('circle')
      .data(fNodes)
      .join('circle')
      .attr('r', (d, i) => d.radius)
      .attr('cx', (d, i) => d.x)
      .attr('cy', (d, i) => d.y)
      .attr('fill', (d, i) => '#000000')
      .style('opacity', 1)
      .on('click', this.newMemorium)
    fSimulation.on('tick', () => {
      fDots.attr('cx', (d) => d.x).attr('cy', (d) => d.y)
    })

    const zoom = d3
      .zoom()
      .scaleExtent([1, 1])
      .on('zoom', function (event) {
        const transform = event.transform
        // const dx = transform.x // % (boxSize * scale)
        // const dy = transform.y // % (boxSize * scale)
        fG.attr(
          'transform',
          'translate(' + transform.x + ',' + transform.y + ')'
        )
      })
    chart.call(zoom).call(zoom.transform, d3.zoomIdentity.scale(1))
  },
  methods: {
    initializeChart() {
      const chart = d3.select('#chart')
      chart
        .append('defs')
        .append('filter')
        .attr('id', 'blur')
        .append('feGaussianBlur')
        .attr('stdDeviation', this.dotBlur)

      this.container = chart.node().parentNode
      this.resizeChart(chart)
      window.addEventListener(
        'resize',
        function () {
          this.resizeChart(chart)
        }.bind(this)
      )
      return chart
    },
    generateDataset(xSize, ySize, minRadius, maxRadius, numDots) {
      const data = []
      for (let i = 0; i < numDots; i++) {
        data[i] = {
          x: Math.floor(Math.random() * xSize),
          y: Math.floor(Math.random() * ySize),
          radius:
            Math.floor(Math.random() * (maxRadius - minRadius + 1)) + minRadius,
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
    newMemorium(event) {
      console.log('clicked')
      console.log(event)
    },
  },
}
</script>

<style>
#chart {
  background-color: #f5f6f5;
}
</style>
