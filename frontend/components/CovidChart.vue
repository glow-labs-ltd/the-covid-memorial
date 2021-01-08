<template>
  <div class="chart-background">
    <svg
      id="chart"
      width="400"
      height="400"
      viewBox="0 0 400 400"
      perserveAspectRatio="xMinYMid"
    ></svg>
  </div>
</template>

<script>
import * as d3 from 'd3'
export default {
  data() {
    return {
      container: null,
      currentWidth: 0,
      currentHeight: 0,
      zoomLevel: 1,
      bgDotBlur: 5,
      bgDotMaxRadius: 18,
      bgDotMinRadius: 6,
      fgDotRadius: 16,
      deceased: [],
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

          const dots = fDots.selectAll('.node')
          for (const dot of dots) {
            const node = d3.select(dot)
            const data = node.data()[0]
            if (data.human) {
              const circle = node.select('circle')
              const image = node.select('image')
              const inViewport = this.isElementInViewport(dot)
              if (inViewport && circle.attr('data-deceased-id') === null) {
                const deceasedToAdd = this.deceased.shift()
                if (deceasedToAdd) {
                  circle.attr('data-deceased-id', deceasedToAdd.id)
                  circle.attr('fill', deceasedToAdd.colour)
                  image.attr('xlink:href', deceasedToAdd.image)
                }
                this.downloadDeceased()
              } else if (!inViewport && circle.attr('data-deceased-id')) {
                circle.attr('data-deceased-id', null)
                circle.attr('fill', '#00000000')
                image.attr('xlink:href', null)
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
      this.container = chart.node().parentNode
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
          const diameter = this.fgDotRadius * 2

          const node = fG
            .append('g')
            .selectAll('.node')
            .data(fNodes)
            .enter()
            .append('g')
            .attr('transform', (d, i) => `translate(${d.x + dx}, ${d.y + dy})`)
            .attr('class', 'node')

          node
            .append('circle')
            .attr('r', (d, i) =>
              d.human ? this.fgDotRadius : this.fgDotRadius * 0.75
            )
            .attr('cx', 0)
            .attr('cy', 0)
            .attr('fill', (d, i) => (d.human ? '#00000000' : '#000000'))
            .attr('data-deceased-id', null)
            .on('click', this.dotClicked)

          node
            .append('defs')
            .append('clipPath')
            .attr('id', 'clip-circle')
            .append('circle')
            .attr('r', (d, i) =>
              d.human ? this.fgDotRadius - 2 : this.fgDotRadius * 0.75
            )
            .attr('cy', 0)
            .attr('cx', 0)

          node
            .append('image')
            .attr('xlink:href', null)
            .attr('x', (d, i) => -this.fgDotRadius + 1)
            .attr('y', (d, i) => -this.fgDotRadius + 1)
            .attr('width', (d, i) => (d.human ? diameter - 2 : diameter * 0.75))
            .attr('height', (d, i) =>
              d.human ? diameter - 2 : diameter * 0.75
            )
            .attr('preserveAspectRatio', 'xMidYMid slice')
            .attr('clip-path', 'url(#clip-circle)')
            .attr('style', 'pointer-events: none')
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
    downloadDeceased() {
      if (this.deceased.length === 0)
        this.deceased = [{ id: 123, image: '/favicon.ico', colour: '#FFCC11' }]
    },
    dotClicked(event, data) {
      if (data.human) {
        const deceasedId = event.toElement.dataset.deceasedId
        if (deceasedId) this.$emit('view', deceasedId)
      } else {
        this.$emit('create')
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-background {
  width: 100vw;
  height: 100vh;
  background-color: $background;
}

#chart {
  background-color: $background;
}
</style>
