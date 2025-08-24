<script>
    import { goto } from "$app/navigation";
</script>

<section style="padding:2rem;max-width:800px;margin:0 auto;">
    <h1>Employer Signup</h1>
    <p>
        This page is under construction. For now, please use the main signup
        flow.
    </p>
    <button class="btn" on:click={() => goto("/")}>Back to Home</button>
</section>

<style>
    .btn {
        padding: 0.6rem 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        cursor: pointer;
    }
</style>
