import React, { Component } from "react";
import { Button, CancelBtn } from "./base";

export class DeployBox extends Component {
  render() {
    return (
      <div id='filedrag'>
        {this.props.message}
      </div>
    )
  }
}

DeployBox.defaultProps = {
  message: "drop files here to deploy"
}

class StartDeployBtn extends Component {
  constructor(props) {
    super(props);

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.deploy();
  }

  render() {
    return (
      <button type='submit'
              disabled={this.props.disabled}
              className='btn btn-rollback'
              onClick={this.handleClick}>
        Start deploy
      </button>
    )
  }
}

class Files extends Component {
  render() {
    var files = this.props.files.map((file) => {
      return (
       <p key={file}>{file}</p>
      );
    });
    return (
      <div id='files'>{files}</div>
    )
  }
}

class Output extends Component {
  render() {
    return (
      <div id='output'>
        <img src="/static/img/ajax-loader.gif" />
        <div className='messages' dangerouslySetInnerHTML={{__html: this.props.message}} />
      </div>
    )
  }
}

export class DeployPopin extends Component {
  constructor(props) {
    super(props);

    this.state  = {
      files: [],
      output: '',
      deploy: false,
      zip: new JSZip(),
      disabled: true
    };

    this.handleDrop = this.handleDrop.bind(this);
    this.cancel = this.cancel.bind(this);
    this.deploy = this.deploy.bind(this);
  }

  handleDrop(e) {
    this.preventDefault(e);

    $('#deploy').on('hide', this.cancel);
    $('#deploy').modal('show');

    var length = e.dataTransfer.items.length;
    for (var i = 0; i < length; i++) {
      var entry = e.dataTransfer.items[i].webkitGetAsEntry();
      if (entry.isFile) {
        this.addFile(entry, this.state.zip);
      } else if (entry.isDirectory) {
        this.addDir(entry, this.state.zip);
      }
    }
    this.setState({disabled: false});
  }

  addFile(entry, zip) {
    if (zip.root.length === 0) {
        var files = this.state.files;
        files.push(entry.fullPath);
        this.setState({files: files});
    }

    this.readFile(entry, (name, result) => {
      zip.file(name, result, {binary: true});
    });
  }

  addDir(entry, zip) {
    var files = this.state.files;

    files.push(entry.fullPath + "/*");
    this.setState({files: files});

    var dirReader = entry.createReader();
    var folder = zip.folder(entry.name);

    dirReader.readEntries((results) => {

      results.forEach((entry) => {

        if (entry.isFile) {
          this.addFile(entry, folder);
        } else {
          this.addDir(entry, folder);
        }

      });
    });
  }

  readFile(entry, callback) {
    entry.file((file) => {
      var reader = new FileReader();

      reader.onloadend = () => {
        callback(entry.name, reader.result);
      };

      reader.readAsBinaryString(file);
    });
  }

  cancel() {
    this.setState({files: [], zip: new JSZip()});
  }

  deploy() {
    this.setState({deploy: true, output: 'Wait until deploy is started.', disabled: true, files: []});

    var content = this.state.zip.generate({type: "base64"});

    var formData = new FormData();
    formData.append("filecontent", content);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', location.pathname, true);
    xhr.onprogress = () => {
      this.setState({output: xhr.responseText});
    }
    xhr.onload = () => {
        setTimeout(() => {
            location.reload();
        }, 2000);
    }
    xhr.send(formData);
  }

  preventDefault(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  componentDidMount() {
    var body = document.getElementsByTagName('body')[0];
    body.addEventListener('drop', this.handleDrop);
    body.addEventListener('dragover', this.preventDefault);
  }

  render() {
    return (
      <div className='deploy-popin'>
      <div className="modal-dialog" role="document">
       <div className="modal-content">
        <div className='modal-header'>
            <h3 id='myModalLabel'>New deploy</h3>
        </div>
        <div className='modal-body'>
            {this.state.deploy ? '' : <DeployBox addFile={this.addFile} message="drop more files here" />}
            {this.state.files.length > 0 ? <Files files={this.state.files} /> : ''}
            {this.state.output.length > 0 ? <Output message={this.state.output} /> : ''}
        </div>
        <div className='modal-footer'>
            <input type='hidden' id='filecontent' name='filecontent' />
            <CancelBtn disabled={this.state.deploy} onClick={this.cancel} />
            <StartDeployBtn deploy={this.deploy} disabled={this.state.disabled} />
          </div>
        </div>
      </div>
    </div>
    )
  }
}

export class RollbackPopin extends Component {
  constructor(props) {
    super(props);

    this.state  = {
      disabled: true,
      output: '',
      rollback: false,
    };

    this.rollback = this.rollback.bind(this);
    this.handleConfirmation = this.handleConfirmation.bind(this);
  }

  rollback(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setState({disabled: true, rollback: true, output: 'Wait until rollback is started.'});
    var xhr = new XMLHttpRequest();
    xhr.open('GET', this.props.url, true);
    xhr.onprogress = () => {
      this.setState({output: xhr.responseText});
    };
    xhr.onload = () => {
        setTimeout(() => {
            location.reload();
        }, 2000);
    }
    xhr.send();
  }

  handleConfirmation(e) {
      this.setState({disabled: e.target.value !== this.props.app})
  }

  render() {
      return (
        <div className="rollback-popin">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className='modal-header'>
                <h3 id='myModalLabel'>Rollback</h3>
              </div>
              <div className='modal-body'>
                {
                    this.state.rollback ? '' :
                        <div>
                            <p>Are you sure you want to rollback your app?</p>
                            <p>Please type in the name of your app to confirm.</p>
                            <input type="text" onChange={this.handleConfirmation} placeholder="app's name" className="remove-confirmation" />
                        </div>
                }
                {this.state.output.length > 0 ? <Output message={this.state.output} /> : ''}
              </div>
              <div className='modal-footer'>
                <CancelBtn disabled={this.state.rollback} />
                <Button text="Rollback" disabled={this.state.disabled} onClick={this.rollback} />
              </div>
            </div>
          </div>
        </div>
      )
  }

 }
