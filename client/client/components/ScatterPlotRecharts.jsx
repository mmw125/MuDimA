import React, { Component } from 'react';
import {ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Dot} from 'recharts';


export default class ScatterPlotRecharts extends React.Component {
    getArticleTooltip(props) {
        const {payload} = props;
        if (payload.length) {
            let story = payload[0]['payload'];
            return (
                <div className="card preview_card"> 
                    <a href={story['link']} style={{textDecoration: 'none'}}>
                        <div style={{background: 'url(' + story['image']+')', backgroundSize: 'cover', backgroundPosition: 'center center', width: '100%', height: '160px', position: 'relative', zIndex: '2'}}>
                        </div>
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Loading_2.gif" width="70%" className="loader_img"/>
                        <div className="card-block">
                          <h4 className="card-text">{story['name']}</h4>
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
             <ScatterChart width={1200} height={1000} margin={{top: 40, right: 20, bottom: 20, left: 20}}>
                <XAxis dataKey={'x'}  hide/>
                <YAxis dataKey={'y'}  hide/>
                <Tooltip cursor={{strokeDasharray: '3 3'}} content={(a,b) => this.getArticleTooltip(a,b)}/>
                <Scatter name='A school' data={this.props.data} fill='#8884d8' onClick={(e) => this.onArticleClicked(e)}/>
            </ScatterChart>
        );
    }
}
