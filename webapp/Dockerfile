
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci || (npm i --package-lock-only && npm ci)
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN npm i -g serve
COPY --from=build /app/dist ./dist
EXPOSE 5173
CMD ["serve","-s","dist","-l","5173"]
