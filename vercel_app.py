{
  "version": 2,
  "builds": [
    {
      "src": "final/asgi.py",
      "use": "@vercel/python"
    },
    {
      "src": "staticfiles/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "staticfiles/$1"
    },
    {
      "src": "/(.*)",
      "dest": "final/asgi.py"
    }
  ]
}
