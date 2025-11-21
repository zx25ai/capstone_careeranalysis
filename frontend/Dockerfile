FROM node:18

WORKDIR /app

COPY package.json .
COPY package-lock.json . 2>/dev/null || true

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
