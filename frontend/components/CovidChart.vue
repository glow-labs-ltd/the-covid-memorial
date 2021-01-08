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
      bZoomLevel: 1,
      bgDotBlur: 5,
      bgDotMaxRadius: 18,
      bgDotMinRadius: 6,
      fDotRadius: 20,
      fZoomLevel: null,
      colours: [
        '#890608',
        '#d4700c',
        '#f3c316',
        '#315e31',
        '#00457a',
        '#470c6e',
        '#72466a',
        '#000000',
      ],
    }
  },
  mounted() {
    // initialize the chart
    const chart = this.initializeChart()

    const shortestEdge = Math.min(this.currentWidth, this.currentHeight)
    this.bgNumDots = Math.floor(shortestEdge)
    this.fgNumDots = Math.floor(shortestEdge / 1.5)
    const boxSize = {
      width: this.currentWidth * 1.5,
      height: this.currentHeight * 1.5,
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

    this.bZoom = d3
      .zoom()
      .scaleExtent([this.bZoomLevel, this.bZoomLevel])
      .on(
        'zoom',
        function (event) {
          bG.attr(
            'transform',
            `translate(${-this.currentWidth / 2}, ${
              -this.currentHeight / 2
            })scale(${event.transform.k})`
          )
        }.bind(this)
      )
    chart.call(this.bZoom.transform, d3.zoomIdentity.scale(this.bZoomLevel))

    // create foreground dots
    const fG = chart.append('g')
    const fData = this.generateDataset(
      boxSize.width,
      boxSize.height,
      this.fDotRadius,
      this.fDotRadius,
      this.fgNumDots,
      true
    )
    const fNodes = fData.map((d) => Object.create(d))
    const fDots = this.drawForegroundDots(fG, fNodes, boxSize)

    this.fZoom = d3
      .zoom()
      .scaleExtent([this.fZoomLevel, this.fZoomLevel])
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

          this.loadDeceased(fDots)
        }.bind(this)
      )
    chart
      .call(this.fZoom)
      .call(this.fZoom.transform, d3.zoomIdentity.scale(this.fZoomLevel))

    this.showInitialDeceased(fDots)
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

      const shortestEdge = Math.min(this.currentWidth, this.currentHeight)
      this.fZoomLevel = -1 / (-shortestEdge / 800)

      if (this.bZoom) {
        chart.call(this.bZoom.transform, d3.zoomIdentity.scale(this.bZoomLevel))
      }

      if (this.fZoom)
        chart.call(this.fZoom.transform, d3.zoomIdentity.scale(this.fZoomLevel))
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
        const human = generateHuman ? Math.random() < 0.8 : false
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
          const diameter = this.fDotRadius * 2

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
              d.human ? this.fDotRadius : this.fDotRadius * 0.75
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
              d.human ? this.fDotRadius - 2 : this.fDotRadius * 0.75
            )
            .attr('cy', 0)
            .attr('cx', 0)

          node
            .append('image')
            .attr('xlink:href', null)
            .attr('x', (d, i) => -this.fDotRadius + 1)
            .attr('y', (d, i) => -this.fDotRadius + 1)
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
    loadDeceased(fDots) {
      const dots = fDots.selectAll('.node')
      for (const dot of dots) {
        const node = d3.select(dot)
        const data = node.data()[0]
        if (data.human) {
          const circle = node.select('circle')
          const image = node.select('image')
          const inViewport = this.isElementInViewport(dot)
          if (inViewport && circle.attr('data-deceased-id') === null) {
            const deceasedToAdd = this.$store.state.deceased[0]
            this.$store.commit('shiftDeceased')
            if (deceasedToAdd) {
              circle.attr('data-deceased-id', deceasedToAdd.id)
              circle.attr('fill', this.colours[deceasedToAdd.colour])
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
    },
    async showInitialDeceased(fDots) {
      if (this.$store.state.deceased.length === 0) {
        await this.$store.dispatch('getDeceased')
      }
      this.loadDeceased(fDots)
    },
    downloadDeceased() {
      if (
        this.$store.state.deceased.length === 0 &&
        !this.$store.state.deceasedLoading
      )
        this.$store.dispatch('getDeceased')
    },
    dotClicked(event, data) {
      if (data.human) {
        const deceasedId = event.toElement.dataset.deceasedId
        if (deceasedId) this.$emit('view', deceasedId)
      } else {
        this.$emit('add')
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
