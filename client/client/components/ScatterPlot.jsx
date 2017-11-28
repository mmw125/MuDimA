// unfinished/src/components/scatter-plot.jsx
import React from 'react';

// Returns the largest X coordinate from the data set
const xMax = (data) => d3.max(data, (d) => d[0]);

// Returns the highest Y coordinate from the data set
const yMax = (data) => d3.max(data, (d) => d[1]);

export default class ScatterPlot extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            scales: {
                xScale: this.props.data[0],
                yScale: this.props.data[1]
            }
        }
    }
    getBoxHtml(e, story) {
        return (
            '<div class="card preview_card"> \
                <a href="'+ story['link'] +'" style="text-decoration: none">  \
                    <div style="background: url('+ story['image'] +'); background-size: cover; background-position: center center; width: 100%; height: 160px; position: relative; z-index: 2"> \
                    </div> \
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Loading_2.gif" width="70%" class="loader_img"/> \
                    <div class="card-block"> \
                      <h4 class="card-text">'+ story['name'] +'</h4> \
                    </div> \
                </a> \
            </div>'
        );
    }
    handleMouseHover(e, story) {
        const d = {
            name: e.target.getAttribute('name'),
            link: e.target.getAttribute('link'),
            x: e.target.getAttribute('x'),
            y: e.target.getAttribute('y')
        };
        d3.select(e.target).attr({fill: "orange"});
        var div = d3.select("body").append("div")
                    .attr('pointer-events', 'none')
                    .attr("class", "tooltip")
                    .style("opacity", 1)
                    .html(this.getBoxHtml(e, story))
                    .style("position", 'absolute')
                    .style("left", ((d.x) - 150 + "px"))
                    .style("top", (d.y + "px"));
    }
	
    handleMouseLeave(e) {
        d3.select('div.tooltip').remove();
        d3.select(e.target).attr({fill: "black"});
    }

    handleMouseClick(e) {
        window.open(e.target.getAttribute('type'), '_blank');
        fetch('http://localhost/userClick', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: e.target.getAttribute('type'),
            })
        });
    }

    xScale() {
        return d3.scale.pow()
            .domain([-1, 1])
            .range([this.props.padding, this.props.width - this.props.padding])
            .exponent(2);
    };

    yScale() {
        return d3.scale.pow()
            .domain([-1, 1])
            .range([this.props.height - this.props.padding, this.props.padding])
            .exponent(2);
    };

    renderCircles() {
        return (story, index) => {
            const coords = [story['x'], story['y']]
            const circleProps = {
                href: story['link'],
                name: story['name'],
                x: this.xScale()(coords[0]),
                y: this.yScale()(coords[1]),
                height: 11 + story['popularity'] / 4,
                width: 11 + story['popularity'] / 4,
                r: 11 + story['popularity'] / 4,
                key: index,
                xlinkHref: story['favicon'],
            };
            return (
				<image 
					{... circleProps}
					onMouseOut={(e) => this.handleMouseLeave(e)}
					onMouseOver={(e) => this.handleMouseHover(e, story)}
					onClick={this.handleMouseClick.bind(this)}
				/> 
 			)
        };
    }

    render() {
        return (
            <svg ref="scatterPlot" width={this.props.width} height={this.props.height}>
                {this.props.data.map(this.renderCircles(this.props))}
            </svg>
        );
    }
}
