<template>
  <div
    class="image-upload__wrapper"
    :class="{ 'drag-shadow': dragging > 0 }"
    @drop.prevent="addDroppedFile"
    @dragover.prevent
    @dragenter.prevent="setDragging(true)"
    @dragend.prevent="setDragging(false)"
    @dragleave.prevent="setDragging(false)"
  >
    <template v-if="previewUrl">
      <vue-cropper
        ref="previewImage"
        :key="previewUrl"
        :src="previewUrl"
        :view-mode="3"
        :guides="false"
        :center="false"
        :highlight="false"
        :background="false"
        :crop-box-movable="false"
        :crop-box-resizable="false"
        :aspect-ratio="1 / 1"
        :auto-crop-area="1"
        :modal="false"
        :repsonsive="false"
        :restore="false"
        drag-mode="move"
        :toggle-drag-mode-on-dblclick="false"
        :min-container-width="30"
        :min-container-height="30"
        class="preview-image"
      />
    </template>
    <template v-else>
      <div class="upload-image" @click="$refs.fileInput.click()">
        <img src="~/assets/images/add-icon.svg" />
      </div>
    </template>
    <div class="instruction">
      <template v-if="!file">
        <h3>Add their photograph</h3>
        <p>Try to use a photo where the person is in the centre of the image</p>
      </template>
      <template v-else>
        <button @click.prevent="$refs.fileInput.click()">
          Choose new photo
        </button>
        <button @click="remove">Remove photo</button>
        <p>You can crop the image by dragging and zooming</p>
      </template>
    </div>
    <input
      ref="fileInput"
      style="display: none"
      type="file"
      accept="image/*"
      @click="resetInput"
      @change="fileSelected"
    />
  </div>
</template>

<script>
import VueCropper from 'vue-cropperjs'
import 'cropperjs/dist/cropper.css'

export default {
  components: {
    VueCropper,
  },
  data() {
    return {
      file: null,
      previewUrl: null,
      maxWidth: 800,
      dragging: 0,
    }
  },
  methods: {
    remove() {
      this.file = null
      this.previewUrl = null
    },
    resetInput(event) {
      event.target.value = null
    },
    fileSelected(event) {
      this.file = event.target.files[0]
      this.createPreviewUrl(this.file)
    },
    createPreviewUrl(file) {
      if (file) {
        this.previewUrl = URL.createObjectURL(this.file)
      }
    },
    addDroppedFile(event) {
      this.file = event.dataTransfer.files[0]
      this.createPreviewUrl(this.file)
      this.setDragging(false)
    },
    setDragging(value) {
      if (value) this.dragging++
      else this.dragging--
    },
    getCroppedImage() {
      if (this.$refs.previewImage) {
        this.$refs.previewImage
          .getCroppedCanvas({ maxWidth: this.maxWidth })
          .toBlob(
            (blob) => {
              const data = {
                blob,
                fileName: this.file?.name?.replace(/\.[^/.]+$/, '.jpg'),
              }
              return data
            },
            'image/jpeg',
            0.85
          )
      }
      return null
    },
  },
}
</script>

<style lang="scss" scoped>
.preview-image {
  height: 16rem;
  width: 16rem;

  ::v-deep .cropper-view-box {
    border: 3px solid black;
    box-sizing: border-box;
    border-radius: 50%;
    outline: 0;
  }

  ::v-deep .cropper-line,
  ::v-deep .cropper-point {
    display: none;
  }

  ::v-deep .cropper-canvas {
    display: none;
  }
}

.image-upload__wrapper {
  display: grid;
  grid-template: auto / 16rem 1fr;
  text-align: left;
  padding: 1rem;

  h3 {
    font-size: 2.5rem;
  }

  .instruction {
    margin: auto 0 auto 3rem;

    p {
      font-size: 1.75rem;
      margin: 1rem 0 0;
      max-width: 32rem;
    }
  }
}

.upload-image {
  cursor: pointer;
}

.drag-shadow {
  transition: outline 0.1s ease-in-out;
  outline: 4px dashed $primary;
}
</style>
