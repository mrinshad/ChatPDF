# Use an official Node image to install and build the app
FROM node:14-alpine as build

# Set working directory in container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy rest of the application code
COPY . .

# Build the React app for production
RUN npm run build

# Use Nginx to serve the files
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
