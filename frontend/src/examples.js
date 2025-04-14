// Python examples
export const pythonExamples = [
    {
      name: 'Simple Bar Chart (Matplotlib)',
      code: `
# Example 1: Simple Bar Chart (Matplotlib)
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
categories = ['A', 'B', 'C', 'D', 'E']
values = [22, 35, 14, 28, 19]

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Create the bar chart
ax.bar(categories, values, color='skyblue')

# Add labels and title
ax.set_xlabel('Categories')
ax.set_ylabel('Values')
ax.set_title('Simple Bar Chart')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)

# Add value labels on top of each bar
for i, v in enumerate(values):
    ax.text(i, v + 0.5, str(v), ha='center')

# Adjust layout
plt.tight_layout()

fig.show()

  `
    },
    {
      name: 'Interactive Scatter Plot (Plotly)',
      code: `
# Example 2: Interactive Scatter Plot (Plotly)
import plotly.express as px
import numpy as np

# Generate random data
np.random.seed(42)
n = 100
x = np.random.normal(0, 1, n)
y = x + np.random.normal(0, 1, n)
sizes = np.random.uniform(5, 15, n)
colors = np.random.uniform(0, 1, n)

df = pd.DataFrame({
    'x_val': x,
    'y_val': y,
    'size': sizes,
    'color': colors
})

# Create a scatter plot with Plotly Express
fig = px.scatter(
    df,
    x='x_val', 
    y='y_val',
    size='size',
    color='color',
    color_continuous_scale='viridis',
    opacity=0.8,
    title='Interactive Scatter Plot',
    labels={'x': 'X Value', 'y': 'Y Value', 'color': 'Color Value'},
    hover_data={'x_val', 'y_val'}
)

# Update layout
fig.update_layout(
    width=800,
    height=600,
    title_font_size=20,
    title_x=0.5,
    coloraxis_colorbar=dict(title='Color Scale')
)

# Update traces
fig.update_traces(
    marker=dict(line=dict(width=1, color='DarkSlateGrey')),
    selector=dict(mode='markers')
)  
fig.show()
  `
    },
    {
      name: '3D Surface Plot (Plotly)',
      code: `
# Example 3: 3D Surface Plot (Plotly)
import plotly.graph_objects as go
import numpy as np

# Create data
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
x_grid, y_grid = np.meshgrid(x, y)

# Create 3D surface
z_grid = np.sin(np.sqrt(x_grid**2 + y_grid**2))

# Create figure
fig = go.Figure(data=[go.Surface(x=x_grid, y=y_grid, z=z_grid)])

# Update layout
fig.update_layout(
    title='3D Surface Plot',
    autosize=False,
    width=800,
    height=600,
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        aspectratio=dict(x=1, y=1, z=0.7),
        camera=dict(
            eye=dict(x=1.2, y=1.2, z=1.2)
        )
    )
)  

fig.show()
  `
    },
    {
      name: 'Line Chart with Multiple Series (Matplotlib)',
      code: `
# Example 4: Line Chart with Multiple Series (Matplotlib)
import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.cos(x)

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data
ax.plot(x, y1, label='sin(x)', color='blue', linewidth=2)
ax.plot(x, y2, label='cos(x)', color='red', linewidth=2)
ax.plot(x, y3, label='sin(x)cos(x)', color='green', linewidth=2, linestyle='--')

# Add labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Multiple Line Series')

# Add grid
ax.grid(True, linestyle='--', alpha=0.7)

# Add legend
ax.legend()

# Adjust layout
plt.tight_layout()  
plt.show()
  `
    }
  ];
  
  // R examples
  export const rExamples = [
    {
      name: 'Basic Bar Chart (ggplot2)',
      code: `
# Example 1: Basic Bar Chart (ggplot2)
# Create a data frame
data <- data.frame(
  category = c("A", "B", "C", "D", "E"),
  value = c(22, 35, 14, 28, 19)
)

# Create a ggplot bar chart
p <- ggplot(data, aes(x = category, y = value, fill = category)) +
  geom_bar(stat = "identity", width = 0.7) +
  geom_text(aes(label = value), vjust = -0.5, size = 4) +
  scale_fill_brewer(palette = "Pastel1") +
  labs(
    title = "Simple Bar Chart",
    x = "Categories",
    y = "Values"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16),
    axis.title = element_text(size = 12),
    legend.position = "none"
  )

# Print the plot
print(p)  
      `
    },
    {
      name: 'Interactive Scatter Plot (plotly)',
      code: `
# Example 2: Interactive Scatter Plot (plotly)
# Load required libraries
library(plotly)

# Create sample data
set.seed(42)
n <- 100
x <- rnorm(n)
y <- x + rnorm(n)
size <- runif(n, 5, 15)
color <- runif(n)

# Create a data frame
data <- data.frame(x = x, y = y, size = size, color = color)

# Create a plotly scatter plot
p <- plot_ly(data,
          x = ~x,
          y = ~y,
          size = ~size,
          color = ~color,
          type = "scatter",
          mode = "markers",
          marker = list(
            opacity = 0.8,
            line = list(width = 1, color = "darkslategrey")
          ),
          hoverinfo = "text",
          text = ~paste("X:", round(x, 2), "<br>Y:", round(y, 2))
        ) %>%
        layout(
          title = "Interactive Scatter Plot",
          xaxis = list(title = "X Value"),
          yaxis = list(title = "Y Value"),
          coloraxis = list(colorbar = list(title = "Color Scale"))
        )

# Print the plot
p

  `
    },
    {
      name: '3D Plot (rgl)',
      code: `
# Example 3: 3D Plot (rgl)
# Load libraries
library(rgl)

# Generate data for a 3D surface
x <- seq(-5, 5, length = 50)
y <- seq(-5, 5, length = 50)
z <- outer(x, y, function(x, y) sin(sqrt(x^2 + y^2)))

# Create colors based on z values
col <- heat.colors(length(z))

# Create a 3D surface
persp3d(x, y, z, col = col,
       xlab = "X Axis", ylab = "Y Axis", zlab = "Z Axis",
       main = "3D Surface Plot")

# Add some points
points3d(x = runif(50, -5, 5),
         y = runif(50, -5, 5),
         z = runif(50, -1, 1),
         col = "blue", size = 4)

  `
    },
    {
      name: 'Boxplot (ggplot2)',
      code: `
# Example 4: Boxplot (ggplot2)
# Create sample data
set.seed(123)
data <- data.frame(
  group = rep(c("A", "B", "C", "D"), each = 30),
  value = c(
    rnorm(30, mean = 5, sd = 1),
    rnorm(30, mean = 7, sd = 1.5),
    rnorm(30, mean = 4, sd = 0.8),
    rnorm(30, mean = 6, sd = 1.2)
  )
)

# Create a boxplot with ggplot2
p <- ggplot(data, aes(x = group, y = value, fill = group)) +
  geom_boxplot(alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.5) +
  scale_fill_brewer(palette = "Set2") +
  labs(
    title = "Boxplot Comparison",
    x = "Group",
    y = "Value"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16),
    axis.title = element_text(size = 12),
    legend.position = "none"
  )

# Print the plot
print(p)    
  `
    }
  ];