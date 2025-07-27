FROM openjdk:21-jdk-slim

WORKDIR /app

# Copy the entire project context
COPY . .

# Make mvnw executable
RUN chmod +x mvnw

# Build the specific module
RUN ./mvnw clean package -pl sbomai-cli -am -DskipTests

# Create a non-root user
RUN addgroup --system javauser && adduser --system --ingroup javauser javauser

# Change ownership of the app directory
RUN chown -R javauser:javauser /app

# Switch to non-root user
USER javauser

# Create directories for SBOM files and reports
RUN mkdir -p /app/sboms /app/reports

# Expose the port (if CLI has a web interface)
EXPOSE 8080

# Default command (can be overridden)
CMD ["java", "-jar", "sbomai-cli/target/sbomai-cli-1.0.0-SNAPSHOT.jar", "--help"] 