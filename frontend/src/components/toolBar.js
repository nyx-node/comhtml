import React, {Component} from "react";
import ReactDOM from "react-dom";
import $ from 'jquery';

const tr= {
  "title":"l-title",
  "description":"l-Description",
  "ssl":"l-SSL",
  "richSnippets":"l-Rich-Snippets",
  "h1":"l-h1",
  "h2":"l-h2",
  "h3":"l-h3",
  "h4":"l-h4",
  "h5":"l-h5",
  "h6":"l-h6",
  "wordCount":"l-Word count",
  "followInfo":"l-Follow Info",
  "noFollow":"l-nofollow",
  "follow":"l-follow",
  "internalLinks":"l-Internal links",
  "linkType":"l-Link Type",
  "identical":"l-Identical",
  "internal":"l-Internal",
  "external":"l-External",
  "images":"l-Images",
  "urlFriendly":"l-Url friendly"}

export default class ToolBar extends Component {
  constructor(props){
    super(props);

  }
  render(){
    return <div className="toolbar">
  <Tabs>
    <Tab label='Basic' include={["title","description","h1","h2","h3","h4","h5","h6","ssl",'urlFriendly']}>
    </Tab>
    <Tab label='Links' include={["followInfo","noFollow","follow","linkType","identical","internal","external"]}>


    </Tab>
    <Tab label='Richsnippet' include={["richSnippets"]}>
    </Tab>
    <Tab label='Images' include={["images"]}>
    </Tab>
    <Tab label='Google Appearance'>
    <Serp />
    </Tab>
  </Tabs>
  </div>
  ;}
}
class Tabs extends Component{
  state ={activeTab: this.props.children[0].props.label}
  changeTab = (tab) => {

    this.setState({ activeTab: tab });
  };
  render(){
    document.getElementById("h-Link Type").style.visibility="hidden";
    document.getElementById("h-Follow Info").style.visibility="hidden";
    document.getElementById("headdings").style.visibility="visible";
    let content;
    let buttons = [];
    Hide();
    return (
      <div>
        {React.Children.map(this.props.children, child =>{
          buttons.push(child.props.label)
          if (child.props.label === this.state.activeTab) {Show(child.props.include);content = child.props.children;}
        })}
        <TabButtons activeTab={this.state.activeTab} buttons={buttons} changeTab={this.changeTab}/>
        <div className="tab-content">{content}</div>
      </div>
    );
  }
}
const TabButtons = ({buttons, changeTab, activeTab}) =>{

  return(
    <div className="tab-buttons">
    {buttons.map(button =>{

       return <button className={button === activeTab? 'bar active': 'bar'} onClick={()=>changeTab(button)}>{button}</button>
    })}
    </div>
  )
}
const Tab = props =>{
  return(
    <React.Fragment>
      {props.children}
    </React.Fragment>
  )
}
const Show=(lines) =>
{
  for (let i in lines) {
    if (document.getElementById(tr[lines[i]])==null){continue;}
    document.getElementById(tr[lines[i]]).style.display="table-row";
  };
}
const Hide= function()
{
  for (const key in tr) {
    if (document.getElementById(tr[key])==null){continue;}
    document.getElementById(tr[key]).style.display="none";

  };
}
{/*https://codepen.io/piotr-modes/pen/ErqdxE*/}

class Serp extends Component {
    constructor(props){
      super(props);
        this.state={title_input:'This is an Example of a Title Tag that is Seventy Characters in length',
        desc_input:"Here is an example of what a snippet looks like in Google's SERPs. The content that appears here is usually taken from the Meta Description tag if relevant.",
        url_input:"www.nyx-compare.com"};
        this.handleInputChange=this.handleInputChange.bind(this);
        this.handleClick=this.handleClick.bind(this);
        this.state.ini_title=this.state.title_input;
        this.state.ini_url=this.state.url_input;
        this.state.ini_desc=this.state.desc_input;

    }
    handleInputChange(e){
      this.setState({[e.target.name]:e.target.value});
    }
    handleClick(e){
      if ((e.target.value==this.state.ini_title)||(e.target.value==this.state.ini_url)||(e.target.value==this.state.ini_desc))
      {e.target.value=''}
      //e.target.value='';
    }

    render(){
      document.getElementById("headdings").style.visibility="hidden";

      const title_len=65;
      const desc_len=150;
      return<div className='serp'>
        <div className='serp-title'>
          <h3>Title</h3><span>{this.state.title_input.length}</span>
          <textarea id='title_input' rows="1" cols="73" name='title_input' onFocus={this.handleClick} onChange={this.handleInputChange} value={this.state.title_input}/>
        </div><div className='serp-title'>
          <h3>URL</h3>
          <textarea id='url_input' rows="1" cols="73" name='url_input' onFocus={this.handleClick} onChange={this.handleInputChange} value={this.state.url_input}/>
        </div><div className='serp-title'>
          <h3>Description</h3><span>{this.state.desc_input.length}</span>
          <textarea id='desc_input' rows="4" cols="73" name='desc_input' onFocus={this.handleClick} onChange={this.handleInputChange} value={this.state.desc_input}/>
        </div>
        <div className='output'>
          <cite>{this.state.url_input}</cite>
          <h4>{(this.state.title_input.length<title_len ? this.state.title_input : this.state.title_input.slice(0,title_len)+"...")}</h4>
          <p>{(this.state.desc_input.length<desc_len ? this.state.desc_input : this.state.desc_input.slice(0,desc_len)+"...")}</p>
        </div>
      </div>;

    }
  }
