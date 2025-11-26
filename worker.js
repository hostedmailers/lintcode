const ROUTES = [
  { prefix: "/lintcode", assetBase: "/lintcode" },
  { prefix: "/big", assetBase: "/big" }
];

const LANDING_PREFIX = "/landing";

export default {
  async fetch(request, env) {
    const originalUrl = new URL(request.url);

    for (const route of ROUTES) {
      if (!matchesPrefix(originalUrl.pathname, route.prefix)) {
        continue;
      }

      const rewrittenUrl = new URL(originalUrl);
      const subPath = normalizeSubPath(originalUrl.pathname.substring(route.prefix.length));
      rewrittenUrl.pathname = `${route.assetBase}${subPath}` || "/";

      const assetRequest = new Request(rewrittenUrl.toString(), request);
      return env.ASSETS.fetch(assetRequest);
    }

    if (!matchesPrefix(originalUrl.pathname, LANDING_PREFIX)) {
      const landingUrl = new URL(originalUrl);
      landingUrl.pathname = `${LANDING_PREFIX}${normalizeSubPath(originalUrl.pathname)}`;
      const landingRequest = new Request(landingUrl.toString(), request);
      const landingResponse = await env.ASSETS.fetch(landingRequest);
      if (landingResponse.status !== 404) {
        return landingResponse;
      }
    }

    return env.ASSETS.fetch(request);
  }
};

function matchesPrefix(pathname, prefix) {
  return pathname === prefix || pathname.startsWith(`${prefix}/`);
}

function normalizeSubPath(subPath) {
  if (!subPath) {
    return "/";
  }
  if (subPath.startsWith("/")) {
    return subPath;
  }
  return `/${subPath}`;
}
