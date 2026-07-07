<script setup lang="ts"></script>

<template>
  <div class="notFound">
    <div>
      <div class="text">抱歉，未找到该页面!</div>
    <div>
      <img src="../../assets/404.gif" alt="" width="500px" height="500px">
    </div>
    </div>
  </div>
</template>

<style>
.notFound{
  height: calc(100vh);
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--newsprint-bg);
  font-family: 'Lora', serif;
  .text{
    display: flex;
    font-size: 25px;
    justify-content: center;
    color: var(--newsprint-neutral-500);
    font-family: 'Playfair Display', serif;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
}
</style>
