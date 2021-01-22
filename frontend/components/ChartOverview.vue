<template>
  <div>
    <transition name="fade-slow" mode="out-in">
      <OverviewInfo v-if="!overviewTransition" />
    </transition>
    <canvas></canvas>
  </div>
</template>

<script>
import * as d3 from 'd3'
import { mapState } from 'vuex'
import { getViewportSize } from '@/utilities/visual'

export default {
  data() {
    return {
      width: null,
      height: null,
      transform: null,
      opacityScale: null,
      canvas: null,
      zoom: null,
      simulation: null,
      minZoom: null,
      maxZoom: null,
      dotSpawner: null,
      startingNumDots: 400,
      radius: d3.randomInt(4, 16),
      transitionTime: 3000,
    }
  },
  computed: {
    ...mapState(['overviewTransition']),
    difference() {
      return this.$store.state.count.today - this.$store.state.count.yesterday
    },
  },
  watch: {
    overviewTransition() {
      if (this.overviewTransition) this.animateOut()
    },
  },
  mounted() {
    this.canvas = d3.select('canvas')
    this.resizeCanvas()
    const context = this.canvas.node().getContext('2d')

    const radii = Array.from({ length: this.startingNumDots }, this.radius)
    const nodes = radii.map((r) => ({ r }))
    this.transform = d3.zoomIdentity
    this.opacityScale = d3
      .scaleLinear()
      .domain([this.minZoom, this.maxZoom])
      .range([1, 0])

    this.simulation = this.setupSimulation(context, nodes)
    this.zoom = this.setupZoom(context, nodes)
    this.animateIn()

    window.addEventListener(
      'resize',
      function () {
        this.resizeCanvas()
      }.bind(this)
    )

    const interval = 900000 / this.difference
    setTimeout(
      function () {
        this.spawnMoreDots(interval, nodes)
      }.bind(this),
      3000
    )
  },
  methods: {
    resizeCanvas() {
      const size = getViewportSize()
      this.width = size.width
      this.height = size.height - 80
      this.canvas.attr('width', this.width).attr('height', this.height)

      const shortestEdge = Math.min(this.width, this.height)
      this.minZoom = shortestEdge / 800
      this.maxZoom = this.minZoom * 6
    },
    setupSimulation(context, nodes) {
      return d3
        .forceSimulation(nodes)
        .alphaTarget(0.2)
        .alphaDecay(0.9)
        .velocityDecay(0.5)
        .force('x', d3.forceX().strength(0.0005))
        .force('y', d3.forceY().strength(0.0005))
        .force(
          'collide',
          d3.forceCollide().radius((d) => d.r + 1.5)
        )
        .on(
          'tick',
          function () {
            this.ticked(context, nodes)
          }.bind(this)
        )
    },
    setupZoom(context, nodes) {
      const zoom = d3
        .zoom()
        .scaleExtent([this.minZoom, this.maxZoom])
        .on(
          'zoom',
          function (event) {
            this.transform = event.transform
            if (this.transform.k >= this.maxZoom) {
              this.navigateToMemoriam()
            }
            this.ticked(context, nodes)
          }.bind(this)
        )
      return zoom
    },
    animateIn() {
      this.canvas
        .call(this.zoom.transform, d3.zoomIdentity.scale(this.maxZoom - 0.01))
        .transition()
        .delay(1500)
        .duration(this.transitionTime)
        .call(this.zoom.transform, d3.zoomIdentity.scale(this.minZoom))
        .on(
          'end',
          function () {
            this.$store.commit('setOverviewTransition', false)
            d3.select(this.canvas.node()).call(this.zoom)
          }.bind(this)
        )
    },
    animateOut() {
      this.canvas
        .transition()
        .duration(this.transitionTime)
        .call(this.zoom.transform, d3.zoomIdentity.scale(this.maxZoom - 0.01))
        .on(
          'end',
          function () {
            this.navigateToMemoriam()
          }.bind(this)
        )
    },
    navigateToMemoriam() {
      this.simulation.stop()
      clearInterval(this.dotSpawner)
      this.$store.commit('setOverviewTransition', false)
      this.$store.commit('setOverview', false)
    },
    spawnMoreDots(interval, nodes) {
      this.dotSpawner = setInterval(
        function () {
          if (this.$store.state.overview) this.addNode(nodes)
        }.bind(this),
        interval
      )
    },
    addNode(nodes) {
      if (nodes.length < this.difference + this.startingNumDots) {
        nodes.push({ r: this.radius() })
        this.simulation.nodes(nodes)
      }
    },
    ticked(context, nodes) {
      context.clearRect(0, 0, this.width, this.height)
      context.save()

      context.globalAlpha = this.opacityScale(this.transform.k)
      context.translate(this.width / 2, this.height / 2)
      context.scale(this.transform.k, this.transform.k)
      context.beginPath()
      for (const d of nodes) {
        context.moveTo(d.x + d.r, d.y)
        context.arc(d.x, d.y, d.r, 0, 2 * Math.PI)
      }
      context.fillStyle = '#333333'
      context.fill()
      context.restore()
    },
  },
}
</script>

<style lang="scss" scoped></style>
