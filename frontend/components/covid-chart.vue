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
      minWidth: 800,
      minHeight: 800,
      zoomLevel: 1,
      bgNumDots: 600,
      bgDotBlur: 5,
      bgDotMaxRadius: 16,
      bgDotMinRadius: 6,
      fgNumDots: 160,
      fgDotRadius: 16,
    }
  },
  mounted() {
    // initialize the chart
    const chart = this.initializeChart()

    // create the background dots
    const bG = chart.append('g')
    const data = this.generateDataset(
      this.currentWidth,
      this.currentHeight,
      this.bgDotMinRadius,
      this.bgDotMaxRadius,
      this.bgNumDots,
      false
    )
    const nodes = data.map((d) => Object.create(d))
    const bSimulation = this.setupCollision(data, 0.3)
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
    bSimulation.on('tick', () => {
      bDots.attr('cx', (d) => d.x).attr('cy', (d) => d.y)
    })

    // create the chart and append the initial dots
    const numBoxes = 4
    const boxSize = {
      width: (Math.max(this.currentWidth, this.currentHeight) * 4) / numBoxes,
      height: (Math.max(this.currentWidth, this.currentHeight) * 4) / numBoxes,
    }

    const fG = chart.append('g')
    const fData = this.generateDataset(
      boxSize.width,
      boxSize.height,
      8,
      8,
      this.fgNumDots,
      true
    )
    const fNodes = fData.map((d) => Object.create(d))
    this.drawForegroundDots(fG, fNodes, boxSize)

    const zoom = d3
      .zoom()
      .scaleExtent([0.01, this.zoomLevel])
      .on('zoom', function (event) {
        const transform = event.transform
        const scale = transform.k
        const dx = transform.x % (boxSize.width * scale)
        const dy = transform.y % (boxSize.height * scale)
        fG.attr(
          'transform',
          'translate(' + dx + ',' + dy + ')scale(' + scale + ')'
        )
      })
    chart.call(zoom).call(zoom.transform, d3.zoomIdentity.scale(this.zoomLevel))
  },
  methods: {
    initializeChart() {
      const chart = d3.select('#chart')
      chart
        .append('defs')
        .append('filter')
        .attr('id', 'blur')
        .append('feGaussianBlur')
        .attr('stdDeviation', this.bgDotBlur)

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
    generateDataset(
      xSize,
      ySize,
      minRadius,
      maxRadius,
      numDots,
      generateHuman
    ) {
      const data = []
      for (let i = 0; i < numDots; i++) {
        data[i] = {
          x: Math.floor(Math.random() * xSize),
          y: Math.floor(Math.random() * ySize),
          radius:
            Math.floor(Math.random() * (maxRadius - minRadius + 1)) + minRadius,
          human: generateHuman ? Math.random() < 0.7 : false,
        }
      }
      return data
    },
    drawForegroundDots(fG, fNodes, boxSize) {
      for (let x = -1; x <= 1; x++) {
        for (let y = -1; y <= 1; y++) {
          const dx = x > 0 ? boxSize.width : x < 0 ? -boxSize.width : 0
          const dy = y > 0 ? boxSize.height : y < 0 ? -boxSize.height : 0
          fG.append('g')
            .selectAll('circle')
            .data(fNodes)
            .join('circle')
            .attr('r', (d, i) =>
              d.human ? this.fgDotRadius : this.fgDotRadius * 0.75
            )
            .attr('cx', (d, i) => d.x + dx)
            .attr('cy', (d, i) => d.y + dy)
            .attr('fill', (d, i) => (d.human ? '#F3C316' : '#000000'))
            .on('click', this.dotClicked)
        }
      }
      return fG
    },
    setupCollision(data, decay) {
      return d3
        .forceSimulation(data)
        .velocityDecay(decay)
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
    dotClicked(event, data) {
      console.log(data)
      if (data.human) {
        console.log('viewing memorium')
        alert('View an existing memorium modal')
      } else {
        console.log('new memorium')
        alert('Create a new memorium modal')
      }
    },
  },
}
</script>

<style>
#chart {
  background-color: #f5f6f5;
}
</style>
