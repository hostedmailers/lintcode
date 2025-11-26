const BASE_PATH = "/locked-lintcode";

export default {
  async fetch(request, env) {
    const originalUrl = new URL(request.url);

    if (!originalUrl.pathname.startsWith(BASE_PATH)) {
      return new Response("Not found", { status: 404 });
    }

    const rewrittenUrl = new URL(originalUrl);
    const strippedPath = originalUrl.pathname.substring(BASE_PATH.length) || "/";
    rewrittenUrl.pathname = strippedPath;

    const assetRequest = new Request(rewrittenUrl.toString(), request);
    return env.ASSETS.fetch(assetRequest);
  }
};
