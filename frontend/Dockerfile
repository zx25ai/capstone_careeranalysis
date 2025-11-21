FROM node:18

WORKDIR /app

# Copy only package.json first
COPY package.json ./

# Install dependencies (skip lock file entirely)
RUN npm install

# Now copy the full frontend source
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
