<template>
  <div>
    <ChartInstructions />
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
import { mapState } from 'vuex'

export default {
  data() {
    return {
      container: null,
      currentWidth: 0,
      currentHeight: 0,
      data: [],
      bNumDots: 25,
      bDotMaxRadius: 36,
      bDotMinRadius: 12,
      fNumDots: 250,
      fDotRadius: 20,
      fMinZoomLevel: null,
      fMaxZoomLevel: null,
      fDotPadding: 6,
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
    }
  },
  computed: mapState(['overviewTransition']),
  watch: {
    overviewTransition() {
      this.$store.commit('setOverview', true)
    },
  },
  mounted() {
    // initialize the chart and variables
    const chart = this.initializeChart()
    const longestEdge = Math.max(this.currentWidth, this.currentHeight)
    const fBoxSize = longestEdge
    const bBoxSize = longestEdge

    // create the background dots
    const bG = chart.append('g')
    const data = this.generateData(
      bBoxSize,
      bBoxSize,
      this.bDotMinRadius,
      this.bDotMaxRadius,
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
    this.humanData = this.data.filter((el) => el.human)
    const fNodes = this.data.map((d) => Object.create(d))
    const fDots = this.setupForegroundNodes(fG, fNodes, fBoxSize)

    this.zoom = this.setupZoom(chart, fDots, fG, bG, fBoxSize, bBoxSize)
    this.animateIn(chart, fDots)
  },
  methods: {
    initializeChart() {
      const chart = d3.select('#chart').attr('opacity', 0)
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

      const pixelRatio = window.devicePixelRatio
      if (pixelRatio > 1) this.fNumDots = Math.floor(this.fNumDots / pixelRatio)

      const shortestEdge = Math.min(this.currentWidth, this.currentHeight)
      this.fMaxZoomLevel = -1 / (-shortestEdge / 800)
      this.fMinZoomLevel = this.fMaxZoomLevel * 0.25

      if (this.zoom)
        chart.call(
          this.zoom.transform,
          d3.zoomIdentity.scale(this.fMaxZoomLevel)
        )
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
        const human = generateHuman ? Math.random() < 0.8 : false
        if (data.length > 0) {
          for (const node of data) {
            const dX = (node.x - x) * (node.x - x)
            const dY = (node.y - y) * (node.y - y)
            const distance = Math.sqrt(dX + dY)
            const dR = node.radius + radius
            const padding = dR + this.fDotPadding
            if (
              distance < padding ||
              x > xSize - this.fDotRadius ||
              x < this.fDotRadius ||
              y > ySize - this.fDotRadius ||
              y < this.fDotRadius
            ) {
              collides = true
              attempts++
              if (attempts > 100) {
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

          bG.append('g')
            .selectAll('circle')
            .data(bNodes)
            .enter()
            .append('circle')
            .attr('r', (d, i) => d.radius)
            .attr('cx', (d, i) => d.x + dx)
            .attr('cy', (d, i) => d.y + dy)
            .attr('fill', '#DDDDDD')
            .attr('class', 'b-node')
            .attr('style', 'will-change: transform;')
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
    setupZoom(chart, fDots, fG, bG, fBoxSize, bBoxSize) {
      const zoom = d3
        .zoom()
        .scaleExtent([this.fMaxZoomLevel - 0.1, this.fMaxZoomLevel])
        .on(
          'zoom',
          function (event) {
            if (event.sourceEvent && this.$store.state.firstTime)
              this.$store.commit('setFirstTime', false)

            const transform = event.transform
            const scale = transform.k
            if (transform.k <= this.fMaxZoomLevel - 0.1)
              this.$store.commit('setOverview', true)

            const fScaleFactor = fBoxSize * scale
            const fdx = transform.x % fScaleFactor
            const fdy = transform.y % fScaleFactor
            fG.attr(
              'transform',
              'translate(' + fdx + ',' + fdy + ')scale(' + scale + ')'
            )

            const bScale = transform.k / 2
            const bScaleFactor = bBoxSize * bScale
            const bdx = (transform.x / 2) % bScaleFactor
            const bdy = (transform.y / 2) % bScaleFactor
            bG.attr(
              'transform',
              'translate(' + bdx + ',' + bdy + ')scale(' + bScale + ')'
            )
          }.bind(this)
        )
        .on(
          'end',
          function (event) {
            if (event.sourceEvent) this.updateDeceasedNodes(fDots)
          }.bind(this)
        )
      chart
        .call(zoom)
        .call(zoom.transform, d3.zoomIdentity.scale(this.fMaxZoomLevel))
      return zoom
    },
    animateIn(chart, fDots) {
      chart.transition().duration(1500).ease(d3.easeLinear).attr('opacity', 1)
      setTimeout(
        function () {
          chart.attr('opacity', 1)
          this.updateDeceasedNodes(fDots)
        }.bind(this),
        1500
      )
    },
    updateDeceasedNodes(fDots) {
      for (const d of this.humanData) {
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
      gsap.ticker.fps(24)
      const dotsToAnimate = gsap.utils.toArray('.b-node')
      dotsToAnimate.forEach((dot) => {
        gsap.set(dot, {
          x: this.randomX(-1),
          y: this.randomX(1),
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
      })
    },
    moveY(target, direction) {
      gsap.to(target, this.randomTime(), {
        y: this.randomY(direction),
        ease: Sine.easeInOut,
        onComplete: this.moveY,
        onCompleteParams: [target, direction * -1],
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
#chart {
  background-color: $background;
}
</style>
