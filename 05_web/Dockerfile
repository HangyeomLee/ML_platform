FROM node:20-slim
WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy all files
COPY . .

# Build the project (optional for dev, but ensures TS is correct)
# RUN npm run build

EXPOSE 5173

# Vite requires --host to be accessible outside the container
CMD ["npm", "run", "dev"]
