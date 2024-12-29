# Use an official Node.js runtime as the base image for building
FROM node:22.11.0 AS builder

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the entire application code
COPY . .

# Build the React app
RUN npm run build

# Use a lightweight web server for the production build
FROM nginx:alpine

# Copy the build output to NGINX's html directory
COPY --from=builder /app/build /usr/share/nginx/html

# Expose the default NGINX port
EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]
