
// Test data
let input = [10, 20, 30, 40, 50, 60];
const categories = ["SemVer_3", "SemVer_2", "V*", "Integer", "Date", "Others"];
const color = d3.scaleOrdinal(d3.schemeCategory10);

const margin = { top: 10, right: 20, bottom: 40, left: 40 };
const width = 500 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

function render(data, selector, categories) {
    const svg = d3.select(selector)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
        .domain(data.map((d, i) => i))
        .rangeRound([0, width])
        .padding(0.1);

    const maxValue = d3.max(data);
    const y = d3.scaleLinear()
        .domain(maxValue === 0 ? [0, 1] : [0, maxValue]) // Handle all-zero data
        .range([height, 0]);

    const yAxis = d3.axisLeft(y)
        .ticks(5)
        .tickFormat(d => (maxValue === 0 ? "0" : d)); // Show only "0" if all data values are zero

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat(i => categories[i]))
        .selectAll(".tick text")
        .attr("class", "axis-label");


    g.append("g")
        .attr("class", "axis axis--y")
        .call(yAxis)
        .append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 10)
        .attr("x", -height / 2)
        .attr("dy", "0.71em")
        .attr("text-anchor", "middle");


    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);  // Initially hidden

    g.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", (d, i) => x(i))
        .attr("y", d => y(d))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d))
        .attr("fill", (d, i) => color(i))
        .on("mouseover", function (event, d) {
            tooltip.transition().duration(200).style("opacity", 0.9);  // Show tooltip
            tooltip.html("Count: " + d)  // Set content
                .style("left", (event.pageX + 0) + "px")  // Position to the right of mouse
                .style("top", (event.pageY - 28) + "px");  // Position above mouse
        })
        // Mouseout event
        .on("mouseout", function () {
            tooltip.transition().duration(200).style("opacity", 0);  // Hide tooltip
        });
}

function update_render(new_input) {
    d3.select("#barchart").selectAll("*").remove();
    render(new_input, "#barchart");
}

render(input, "#barchart", categories);

let input_2 = [30, 40]
const categories_2 = ["URL", "Non-URL"]
render(input_2, "#barchart2", categories_2)

// Test button for selenium

