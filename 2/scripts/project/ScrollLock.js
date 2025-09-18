runOnStartup(async runtime => {

  runtime.addEventListener("beforeprojectstart", () => OnBeforeProjectStart(runtime));
});

{
  window.addEventListener('keydown', ev => {
    if (['ArrowDown', 'ArrowUp', ' '].includes(ev.key)) {
      ev.preventDefault();
    }
  });
  window.addEventListener('wheel', ev => ev.preventDefault(), {
    passive: false
  });

}

async function OnBeforeProjectStart(runtime) {

  runtime.addEventListener("tick", () => Tick(runtime));
}

function Tick(runtime) {

}