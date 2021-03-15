import React, {Component} from "react";
import ReactDOM from "react-dom";

export default class FormApp extends Component {
  constructor(props){
    super(props);
    this.state={nb_url:2};
    this.addInput = this.addInput.bind(this);
  }
  addInput(){

    this.setState((state)=>(this.state.nb_url>=5 ? {nb_url:5} : {nb_url:this.state.nb_url+1}));
  }
  render(){
    const items =[]
    let l=0
    for (let i = 0; i < this.state.nb_url-1; i++) {
    l=i+1;
    items.push(<section>
      <h2>Url {l}</h2>
      <input type="text" name={"url"+l} required />
    </section>)};
    items.push(<section>
      <h2>Url {this.state.nb_url}</h2>
      <input type="text" name={"url"+this.state.nb_url}  required />
      {this.state.nb_url==5 ? '': <button type='button' id="plus" onClick={this.addInput}>+</button>}
    </section>);

    return <div>
      {items}


    </div>;
  }
}
