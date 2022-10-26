<template>
  <div class="container mt-4">
    <div class="row d-flex">
      <div class="col d-flex">
        <div>
          <button
            @click="data.eraser = false"
            class="form-control btn btn-secondary"
            :class="{ active: !data.eraser }"
          >
            Draw
          </button>
          <button
            @click="data.eraser = true"
            class="form-control btn btn-secondary"
            :class="{ active: data.eraser }"
          >
            Erase
          </button>
          <select v-model="data.line" class="form-control">
            <option v-for="n in 25" :key="'option-' + n" :value="n">
              {{ n }}
            </option>
          </select>
          <input type="color" v-model="data.color" class="form-control" />
          <button
            type="button"
            @click.prevent="$refs.VueCanvasDrawing.reset()"
            class="form-control btn btn-secondary"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-file-earmark"
              viewBox="0 0 16 16"
            >
              <path
                d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5h-2z"
              />
            </svg>
            Reset
          </button>
        </div>
        <div class="flex-grow-1">
          <VueDrawingCanvas
            ref="VueCanvasDrawing"
            v-model:image="data.image"
            :stroke-type="data.strokeType"
            :line-cap="data.lineCap"
            :line-join="data.lineJoin"
            :fill-shape="data.fillShape"
            :eraser="data.eraser"
            :lineWidth="data.line"
            :color="data.color"
            :background-color="data.backgroundColor"
            :lock="data.disabled"
          />
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <h3>Output:</h3>
        <img :src="data.image" style="border: solid 1px #000000" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import VueDrawingCanvas from "vue-drawing-canvas";
import { reactive } from "vue";

const data = reactive({
  image: "",
  eraser: false,
  disabled: false,
  fillShape: false,
  line: 20,
  color: "#be0b0b",
  strokeType: "dash",
  lineCap: "round",
  lineJoin: "round",
  backgroundColor: "#FFFFFF",
  backgroundImage: null,
  watermark: null,
  additionalImages: [],
});

async function callAPI() {
  const result = await fetch("http://127.0.0.1:8000/test");
  console.log(await result.json());
}

callAPI();
</script>

<style lang="scss">
.active {
  background-color: rgb(165, 51, 226) !important;
  color: black !important;
}
</style>
