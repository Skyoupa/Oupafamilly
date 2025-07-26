FROM node:16-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN yarn build

# Serve the application
RUN yarn global add serve
EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
