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
      bgDotMaxRadius: 18,
      bgDotMinRadius: 6,
      fgNumDots: 160,
      fgDotRadius: 16,
    }
  },
  mounted() {
    // initialize the chart
    const chart = this.initializeChart()
    this.bgNumDots = Math.floor(
      Math.min(this.currentWidth, this.currentHeight) / 6
    )
    this.fgNumDots = Math.floor(
      Math.min(this.currentWidth, this.currentHeight) / 8
    )

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
    bG.append('g')
      .attr('filter', 'url(#blur)')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', (d, i) => d.radius)
      .attr('cx', (d, i) => d.x)
      .attr('cy', (d, i) => d.y)
      .attr('fill', '#000000')
      .style('opacity', 0.6)

    // create the chart and append the initial dots
    const numBoxes = 4
    const boxSize = {
      width: (Math.max(this.currentWidth, this.currentHeight) * 3) / numBoxes,
      height: (Math.max(this.currentWidth, this.currentHeight) * 3) / numBoxes,
    }

    const fG = chart.append('g')
    const fData = this.generateDataset(
      boxSize.width,
      boxSize.height,
      this.fgDotRadius,
      this.fgDotRadius,
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
      let i = 0
      let attempts = 0
      while (i < numDots) {
        let collides = false
        const x = Math.floor(Math.random() * xSize)
        const y = Math.floor(Math.random() * ySize)
        const radius =
          Math.floor(Math.random() * (maxRadius - minRadius + 1)) + minRadius
        const human = generateHuman ? Math.random() < 0.6 : false
        if (data.length > 0) {
          for (const node of data) {
            const dX = (node.x - x) * (node.x - x)
            const dY = (node.y - y) * (node.y - y)
            const dR = node.radius + radius
            if (Math.sqrt(dX + dY) < dR * 2 + 40) {
              collides = true
              attempts++
              if (attempts > 2) {
                i++
              }
            }
          }
        }

        if (!collides) {
          data.push({ x, y, radius, human })
          i++
          attempts = 0
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
