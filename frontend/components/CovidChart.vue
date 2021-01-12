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
import { gsap, Sine } from 'gsap'

export default {
  data() {
    return {
      container: null,
      currentWidth: 0,
      currentHeight: 0,
      data: [],
      bNumDots: 50,
      bgDotMaxRadius: 18,
      bgDotMinRadius: 6,
      fNumDots: 300,
      fDotRadius: 20,
      fZoomLevel: null,
      fDotPadding: 10,
      inViewportPadding: 100,
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
      randomX: this.random(1, 5),
      randomY: this.random(1, 5),
      randomTime: this.random(1, 3),
      randomTime2: this.random(3, 6),
    }
  },
  mounted() {
    // initialize the chart and variables
    const chart = this.initializeChart()
    const longestEdge = Math.max(this.currentWidth, this.currentHeight)
    const fBoxSize = longestEdge
    const bBoxSize = longestEdge / 2

    // create the background dots
    const bG = chart.append('g')
    const data = this.generateData(
      bBoxSize,
      bBoxSize,
      this.bgDotMinRadius,
      this.bgDotMaxRadius,
      this.bNumDots,
      false
    )
    const bNodes = data.map((d) => Object.create(d))
    this.setupBackgroundNodes(bG, bNodes, bBoxSize)
    this.setupBackgroundAnimation()

    // create foreground dots
    const fG = chart.append('g')
    this.data = this.generateData(
      fBoxSize,
      fBoxSize,
      this.fDotRadius,
      this.fDotRadius,
      this.fNumDots,
      true
    )
    const fNodes = this.data.map((d) => Object.create(d))
    const fDots = this.setupForegroundNodes(fG, fNodes, fBoxSize)

    this.fZoom = d3
      .zoom()
      .scaleExtent([this.fZoomLevel, this.fZoomLevel])
      .on('zoom', function (event) {
        const transform = event.transform
        const scale = transform.k

        const fScaleFactor = fBoxSize * scale
        const fdx = transform.x % fScaleFactor
        const fdy = transform.y % fScaleFactor
        fG.attr(
          'transform',
          'translate(' + fdx + ',' + fdy + ')scale(' + scale + ')'
        )

        const bScaleFactor = bBoxSize * scale
        const bdx = (transform.x / 2) % bScaleFactor
        const bdy = (transform.y / 2) % bScaleFactor
        bG.attr(
          'transform',
          'translate(' + bdx + ',' + bdy + ')scale(' + scale + ')'
        )
      })
      .on(
        'end',
        function (event) {
          this.updateDeceasedNodes(fDots)
        }.bind(this)
      )
    chart
      .call(this.fZoom)
      .call(this.fZoom.transform, d3.zoomIdentity.scale(this.fZoomLevel))

    this.downloadInitialDeceased(fDots)
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
      this.currentWidth = window.innerWidth
      this.currentHeight = window.innerHeight
      chart.attr('width', this.currentWidth)
      chart.attr('height', this.currentHeight)

      const shortestEdge = Math.min(this.currentWidth, this.currentHeight)
      this.fZoomLevel = -1 / (-shortestEdge / 800)

      if (this.bZoom) {
        chart.call(this.bZoom.transform, d3.zoomIdentity.scale(this.fZoomLevel))
      }

      if (this.fZoom)
        chart.call(this.fZoom.transform, d3.zoomIdentity.scale(this.fZoomLevel))
    },
    generateData(xSize, ySize, minRadius, maxRadius, numDots, generateHuman) {
      const data = []
      let i = 0
      let attempts = 0
      while (i < numDots) {
        let collides = false
        const x = Math.floor(Math.random() * xSize)
        const y = Math.floor(Math.random() * ySize)
        const radius =
          Math.floor(Math.random() * (maxRadius - minRadius + 1)) + minRadius
        const human = generateHuman ? Math.random() < 0.7 : false
        if (data.length > 0) {
          for (const node of data) {
            const dX = (node.x - x) * (node.x - x)
            const dY = (node.y - y) * (node.y - y)
            const dR = node.radius + radius
            if (
              Math.sqrt(dX + dY) < dR * 2 + this.fDotPadding ||
              x > xSize - this.fDotPadding ||
              x < this.fDotPadding ||
              y > ySize - this.fDotPadding ||
              y < this.fDotPadding
            ) {
              collides = true
              attempts++
              if (attempts > 2) {
                i++
              }
            }
          }
        }

        if (!collides) {
          data.push({ id: i, x, y, radius, human, deceasedId: null })
          attempts = 0
          i++
        }
      }
      return data
    },
    setupBackgroundNodes(bG, bNodes, boxSize) {
      for (let x = -1; x <= 1; x++) {
        for (let y = -1; y <= 1; y++) {
          const dx = x > 0 ? boxSize : x < 0 ? -boxSize : 0
          const dy = y > 0 ? boxSize : y < 0 ? -boxSize : 0

          const node = bG
            .append('g')
            // .attr('filter', 'url(#blur)')
            .selectAll('circle')
            .data(bNodes)
            .enter()
            .append('g')
            .attr('transform', (d, i) => `translate(${d.x + dx}, ${d.y + dy})`)

          node
            .append('circle')
            .attr('r', (d, i) => d.radius)
            .attr('cx', (d, i) => d.x)
            .attr('cy', (d, i) => d.y)
            .attr('fill', '#000000')
            .attr('class', 'b-node')
            .style('opacity', 0.1)
        }
      }
      return bG
    },
    setupForegroundNodes(fG, fNodes, boxSize) {
      for (let x = -1; x <= 1; x++) {
        for (let y = -1; y <= 1; y++) {
          const dx = x > 0 ? boxSize : x < 0 ? -boxSize : 0
          const dy = y > 0 ? boxSize : y < 0 ? -boxSize : 0
          const diameter = this.fDotRadius * 2

          const node = fG
            .append('g')
            .selectAll('.node')
            .data(fNodes)
            .enter()
            .append('g')
            .attr('transform', (d, i) => `translate(${d.x + dx}, ${d.y + dy})`)
            .attr('opacity', (d, i) => (d.human ? 0 : 1))
            .attr('class', (d, i) => `node node-${d.id.toString()}`)

          node
            .append('circle')
            .attr('r', this.fDotRadius)
            .attr('cx', 0)
            .attr('cy', 0)
            .attr('fill', '#00000000')
            .attr('style', 'cursor: pointer;')
            .attr('class', 'dot-background')
            .on('click', this.nodeClicked)

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
            .attr('xlink:href', (d, i) =>
              d.human ? null : require('~/assets/images/add-icon.svg')
            )
            .attr('x', (d, i) =>
              d.human ? -this.fDotRadius + 1 : -this.fDotRadius + 5
            )
            .attr('y', (d, i) =>
              d.human ? -this.fDotRadius + 1 : -this.fDotRadius + 5
            )
            .attr('width', (d, i) => (d.human ? diameter - 2 : diameter * 0.75))
            .attr('height', (d, i) =>
              d.human ? diameter - 2 : diameter * 0.75
            )
            .attr('preserveAspectRatio', 'xMidYMid slice')
            .attr('clip-path', 'url(#clip-circle)')
            .attr('style', 'pointer-events: none;')
            .attr('class', 'dot-image')
        }
      }
      return fG
    },
    updateDeceasedNodes(fDots) {
      for (const d of this.data.filter((el) => el.human)) {
        const dotsToCheck = fDots.selectAll(`.node-${d.id.toString()}`)
        let visible = false
        for (const dot of dotsToCheck) {
          if (this.isElementInViewport(dot)) {
            visible = true
            break
          }
        }

        if (visible && !d.deceasedId) {
          const deceasedToAdd = this.$store.state.deceased[0]
          this.$store.commit('shiftDeceased')
          if (deceasedToAdd) {
            dotsToCheck
              .select('.dot-background')
              .attr('fill', this.colours[deceasedToAdd.colour])
            dotsToCheck
              .select('.dot-image')
              .attr('xlink:href', deceasedToAdd.image)
            dotsToCheck
              .transition()
              .attr('opacity', 1)
              .duration(1000)
              .delay(500)
            d.deceasedId = deceasedToAdd.slug
          }
          this.downloadDeceased()
        } else if (!visible && d.deceasedId) {
          dotsToCheck.select('.dot-background').attr('fill', '#00000000')
          dotsToCheck.select('.dot-image').attr('xlink:href', null)
          dotsToCheck.attr('opacity', 0)
          d.deceasedId = null
        }
      }
    },
    async downloadInitialDeceased(fDots) {
      if (this.$store.state.deceased.length === 0) {
        await this.$store.dispatch('getDeceased')
      }
      this.updateDeceasedNodes(fDots)
    },
    downloadDeceased() {
      if (
        this.$store.state.deceased.length === 0 &&
        !this.$store.state.deceasedLoading
      )
        this.$store.dispatch('getDeceased')
    },
    nodeClicked(event, data) {
      if (data.human) {
        if (data.deceasedId) this.$emit('view', data.deceasedId)
      } else {
        this.$emit('add')
      }
    },
    isElementInViewport(el) {
      const bounds = el.getBoundingClientRect()
      return (
        bounds.top >= -this.inViewportPadding &&
        bounds.left >= -this.inViewportPadding &&
        bounds.bottom <= this.currentHeight + this.inViewportPadding &&
        bounds.right <= this.currentWidth + this.inViewportPadding
      )
    },
    setupBackgroundAnimation() {
      const dotsToAnimate = gsap.utils.toArray('.b-node')
      dotsToAnimate.forEach((dot) => {
        gsap.set(dot, {
          x: this.randomX(-1),
          y: this.randomX(1),
          force3D: true,
        })

        this.moveX(dot, 1)
        this.moveY(dot, -1)
      })
    },
    moveX(target, direction) {
      gsap.to(target, this.randomTime(), {
        x: this.randomX(direction),
        ease: Sine.easeInOut,
        onComplete: this.moveX,
        onCompleteParams: [target, direction * -1],
        force3D: true,
      })
    },
    moveY(target, direction) {
      gsap.to(target, this.randomTime(), {
        y: this.randomY(direction),
        ease: Sine.easeInOut,
        onComplete: this.moveY,
        onCompleteParams: [target, direction * -1],
        force3D: true,
      })
    },
    random(min, max) {
      const delta = max - min
      return (direction = 1) => (min + delta * Math.random()) * direction
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
