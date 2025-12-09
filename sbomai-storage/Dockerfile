FROM eclipse-temurin:21-jdk

WORKDIR /app

# Copy the entire project context
COPY . .

# Make mvnw executable
RUN chmod +x mvnw

# Build the specific module
RUN ./mvnw clean package -pl sbomai-storage -am -DskipTests

# Create a non-root user
RUN addgroup --system javauser && adduser --system --ingroup javauser javauser

# Change ownership of the app directory
RUN chown -R javauser:javauser /app

# Switch to non-root user
USER javauser

# Expose the port
EXPOSE 8082

# Run the application
CMD ["java", "-jar", "sbomai-storage/target/sbomai-storage-1.0.0-SNAPSHOT.jar"]

