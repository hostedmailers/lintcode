const ROUTES = [
  { prefix: "/lintcode", assetBase: "/lintcode" },
  { prefix: "/big", assetBase: "/big" }
];

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
