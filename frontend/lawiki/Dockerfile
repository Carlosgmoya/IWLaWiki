# Use the specific Node.js version 22.11.0 as a parent image
FROM node:22.11.0 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire application
COPY . .

# Expose the port where React development server will run (default is 3000)
EXPOSE 3000

# Run the React development server
CMD ["npm", "start"]
