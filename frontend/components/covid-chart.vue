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
      bgDotBlur: 5,
      bgDotMaxRadius: 18,
      bgDotMinRadius: 6,
      fgDotRadius: 16,
    }
  },
  mounted() {
    // initialize the chart
    const chart = this.initializeChart()

    const longestEdge = Math.max(this.currentWidth, this.currentHeight)
    this.bgNumDots = Math.floor(longestEdge)
    this.fgNumDots = Math.floor(longestEdge / 2)
    const boxSize = {
      width: this.currentWidth * 2,
      height: this.currentHeight * 2,
    }
    this.zoomLevel = this.zoomLevel * (-1 / (-longestEdge / 1600))

    // create the background dots
    const bG = chart.append('g')
    const data = this.generateDataset(
      boxSize.width,
      boxSize.height,
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

    // create foreground dots
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
    const fDots = this.drawForegroundDots(fG, fNodes, boxSize)

    const zoom = d3
      .zoom()
      .scaleExtent([this.zoomLevel, this.zoomLevel])
      .on(
        'zoom',
        function (event) {
          const transform = event.transform
          const scale = transform.k
          const dx = transform.x % (boxSize.width * scale)
          const dy = transform.y % (boxSize.height * scale)
          fG.attr(
            'transform',
            'translate(' + dx + ',' + dy + ')scale(' + scale + ')'
          )

          const dots = fDots.selectAll('circle')
          for (const dot of dots) {
            const node = d3.select(dot)
            const data = node.data()[0]
            if (data.human) {
              const inViewport = this.isElementInViewport(dot)
              if (inViewport && !data.visible) {
                node.attr('fill', '#11CCFF')
                data.visible = true
              }
            }
          }
        }.bind(this)
      )
    chart.call(zoom).call(zoom.transform, d3.zoomIdentity.scale(this.zoomLevel))

    const zoomBg = d3
      .zoom()
      .scaleExtent([this.zoomLevel, this.zoomLevel])
      .on('zoom', function (event) {
        bG.attr('transform', 'scale(' + event.transform.k + ')')
      })
    chart.call(zoomBg.transform, d3.zoomIdentity.scale(this.zoomLevel))
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
    resizeChart(chart) {
      this.currentWidth = this.container.getBoundingClientRect().width
      this.currentHeight = this.container.getBoundingClientRect().height
      chart.attr('width', this.currentWidth)
      chart.attr('height', this.currentHeight)
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
        const colour = human ? '#F3C316' : '#000000'
        const visible = false
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
          data.push({ x, y, radius, human, colour, visible })
          attempts = 0
          i++
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
            .attr('fill', (d, i) => d.colour)
            .on('click', this.dotClicked)
          /*
            .append('svg:image')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', 24)
            .attr('height', 24)
            .attr('xlink:href', (d, i) =>
              d.human ? 'https://www.w3schools.com/w3images/avatar6.png' : null
            )
            */
        }
      }
      return fG
    },
    isElementInViewport(el) {
      const rect = el.getBoundingClientRect()
      return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= this.currentHeight &&
        rect.right <= this.currentWidth
      )
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
