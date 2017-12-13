import React, { Component } from 'react';
import {ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Dot} from 'recharts';
const scatter_styles = {
    width: 1200,
    height: 1000
}
const CustomizedShape = (props) => {
    let {cx, cy, favicon, popularity, source, payload} = props;
    const height = 2 * (11 + popularity / 5);
    const width = 2 * (11 + popularity / 5);
    // Adjust cx and cy to position the lines in the center
    cx = cx - (width/2);
    cy = cy - (height/2);
    favicon = favicon ? favicon : "https://upload.wikimedia.org/wikipedia/commons/3/3f/Article_icon_cropped.svg";
    return (
        <g>
          <g transform={`translate(${cx},${cy})`}>
            <image href={favicon} height={height} width={width}/>
          </g>
        </g>
    );
};
const xScale = () => {
    return d3.scale.pow()
        .domain([-1, 1])
        .range([20, 1200-20])
        
};

const yScale = () => {
    return d3.scale.pow()
        .domain([-1, 1])
        .range([1000 - 20, 20])
        
};
export default class ScatterPlotRecharts extends React.Component {
    constructor(props) {
        super(props);
    }
    getArticleTooltip(props, b) {
        const {payload} = props;
        if (payload.length) {
            let story = payload[0]['payload'];
            let image_div = (
                <div>
                    <div style={{background: 'url(' + story['image']+')', backgroundSize: 'cover', backgroundPosition: 'center center', width: '100%', height: '160px', position: 'relative', zIndex: '2'}}>
                    </div>
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Loading_2.gif" width="70%" className="loader_img"/>
                </div>
            );
            image_div = story['image'] ? image_div : null;
            return (
                <div className="card preview_card"> 
                    <a href={story['link']} style={{textDecoration: 'none'}}>
                        {image_div}
                        <div className="card-block">
                            <h6 className="card-text">{story['source']}</h6>
                            <h6 className="card-text">{story['name']}</h6>
                        </div>
                    </a>
                </div>
            );
        }
    }

    onArticleClicked(e) {
        window.open(e.link, '_blank');
    }

    render() {
        return (
            <ScatterChart width={scatter_styles.width} height={scatter_styles.height} margin={{top: 40, right: 20, bottom: 20, left: 20}}>
                <XAxis dataKey={'x'}  hide/>
                <YAxis dataKey={'y'}  hide/>
                <Tooltip  cursor={{strokeDasharray: '3 3'}} content={(a,b) => this.getArticleTooltip(a,b)}/>
                <Scatter isAnimationActive={false} data={this.props.data} fill='#8884d8' onClick={(e) => this.onArticleClicked(e)} shape={<CustomizedShape />}/>
            </ScatterChart>
        );
    }
}
