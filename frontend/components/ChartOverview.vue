<template>
  <canvas></canvas>
</template>

<script>
import * as d3 from 'd3'

export default {
  data() {
    return {
      transform: null,
    }
  },
  mounted() {
    const width = window.innerWidth
    const height = window.innerHeight - 60
    const canvas = d3
      .select('canvas')
      .attr('width', width)
      .attr('height', height)
    const context = canvas.node().getContext('2d')

    const radii = Array.from({ length: 1200 }, d3.randomUniform(4, 16))
    const nodes = radii.map((r) => ({ r }))
    this.transform = d3.zoomIdentity

    d3.forceSimulation(nodes)
      .velocityDecay(0.2)
      .force('x', d3.forceX().strength(0.002))
      .force('y', d3.forceY().strength(0.002))
      .force(
        'collide',
        d3
          .forceCollide()
          .radius((d) => d.r + 0.5)
          .iterations(2)
      )
      .on(
        'tick',
        function () {
          this.ticked(context, nodes, width, height)
        }.bind(this)
      )

    d3.select(canvas.node()).call(
      d3
        .zoom()
        .scaleExtent([1, 1.6])
        .on(
          'zoom',
          function (event) {
            this.transform = event.transform
            if (this.transform.k > 1.5) {
              this.$emit('zoomIn')
            }
            this.ticked(context, nodes, width, height)
          }.bind(this)
        )
    )
  },
  methods: {
    ticked(context, nodes, width, height) {
      context.clearRect(0, 0, width, height)
      context.save()
      context.scale(this.transform.k, this.transform.k)
      context.globalAlpha = 1 + 1 - this.transform.k
      context.translate(width / 2, height / 2)
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
