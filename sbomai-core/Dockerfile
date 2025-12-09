FROM eclipse-temurin:21-jdk

WORKDIR /app

# Copy the entire project context
COPY . .

# Make mvnw executable
RUN chmod +x mvnw

# Build the specific module
RUN ./mvnw clean package -pl sbomai-core -am -DskipTests

# Create a non-root user
RUN addgroup --system javauser && adduser --system --ingroup javauser javauser

# Change ownership of the app directory
RUN chown -R javauser:javauser /app

# Switch to non-root user
USER javauser

# Expose the port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "sbomai-core/target/sbomai-core-1.0.0-SNAPSHOT.jar"] 