<script lang="ts">
	import { Play ,Dislike, Warning,Error} from "@gradio/icons";

	import { onMount,onDestroy } from "svelte";

	export let handle_action: (selected: string | null) => void;

	export let j:boolean;
	export let enableSecurity:boolean;

	let selected: "run" | "notrun" | null = null;
	let copied = false;
	let isSecure:boolean;
	let timer: NodeJS.Timeout;
	function copy_feedback(): void {
		copied = true;
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => {
			copied = false;
		}, 2000);
	}

	let secure = !enableSecurity;

	function onSecUpdated(customEventWithTitle) {
		
        secure = customEventWithTitle.detail.isSecure;
		isSecure=secure
		console.log('sec is ',secure)

		}


	onMount(
		
			function () {
				if(j){
					document.addEventListener("secUpdated", onSecUpdated);

					return () => {
							document.removeEventListener("secUpdated", onSecUpdated);
					}
				}
			}
		
	);



	

	onDestroy(() => {
		if (timer) clearTimeout(timer);
	});
</script>

<button
	on:click={() => {
		if(isSecure ||!enableSecurity && j){
			selected = "run";
			handle_action(selected);
		}

		copy_feedback();
	}}

>
	{#if secure}
	{#if !copied}
	<Play selected={false} isLast={j}/>
	{/if}
	{#if copied}
	<Play selected={selected === "run"} isLast={j}/>
	{/if}
	{:else}
	<Play selected={false} isLast={j}/>

	{/if}
</button>
{#if enableSecurity}
<button>
	
	<Warning secure={isSecure} isLast={j}/>
	
</button>
{/if}

<style>
	button {
		position: relative;
		top: 0;
		right: 0;
		cursor: pointer;
		color: var(--body-text-color-subdued);
		width: 17px;
		height: 17px;
		margin-right: 5px;
	}



</style>
