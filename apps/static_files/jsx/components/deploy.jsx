var React = require('react');

var DeployBox = React.createClass({
  render: function() {
    return (
      <div id='filedrag'>
        drop files here to deploy
      </div>
    );
  }
});

var StartDeployBtn = React.createClass({
  getInitialState: function() {
    return {disabled: false};
  },
  handleClick: function() {
    this.setState({disabled: true});
    this.props.deploy();
  },
  render: function() {
    return (
      <button type='submit'
              disabled={this.state.disabled}
              className='btn btn-danger btn-rollback'
              onClick={this.handleClick}>
        Start deploy
      </button>
    )
  }
});

var CancelBtn = React.createClass({
  render: function() {
    return (
      <button disabled={this.props.disabled}
              data-dismiss='modal'
              aria-hidden='true'
              className='btn'>
        Cancel
      </button>
    )
  }
});

var Files = React.createClass({
  render: function() {
    var files = this.props.files.map(function(file) {
      return (
       <p>{file}</p> 
      );
    });
    return (
      <div id='files'>{files}</div>
    )
  }
});

var Output = React.createClass({
  render: function() {
    return (
      <div id='output'dangerouslySetInnerHTML={{__html: this.props.message}} />
    )
  }
});

var DeployPopin = React.createClass({
  handleDrop: function(e) {
    this.preventDefault(e);

    $('#deploy').modal('show');

    var length = e.dataTransfer.items.length;
    for (var i = 0; i < length; i++) {
      var entry = e.dataTransfer.items[i].webkitGetAsEntry();
      if (entry.isFile) {
        this.addFile(entry);
      } else if (entry.isDirectory) {
        this.addDir(entry);
      }
    }
  },
  addFile: function(entry) {
    var files = this.state.files;

    files.push(entry.name);
    this.setState({files: files});

    this.readFile(entry, function(name, result) {
      this.state.zip.file(name, result, {binary: true});
    }.bind(this));
  },
  addDir: function(entry) {
    var files = this.state.files;

    var dirName = entry.name + "/";
    files.push(dirName);
    this.setState({files: files});

    var dirReader = entry.createReader();
    var folder = this.state.zip.folder(entry.name);
    dirReader.readEntries (function(results) {
      results.forEach(function(entry) {
        files.push(dirName + entry.name);
        this.setState({files: files});

        this.readFile(entry, function(name, result) {
          folder.file(name, result, {binary: true});
        });
      }.bind(this));
    }.bind(this));
  },
  readFile: function(entry, callback) {
    entry.file(function(file) {
      var reader = new FileReader();

      reader.onloadend = function() {
        callback(entry.name, this.result);
      };

      reader.readAsBinaryString(file);
    });
  },
  getInitialState: function() {
    return {files: [], output: '', deploy: false, zip: new JSZip()};
  },
  deploy: function() {
    this.setState({deploy: true, output: 'Wait until deploy is started.'});

    var content = this.state.zip.generate({type: "base64"});

    var formData = new FormData();
    formData.append("filecontent", content);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', location.pathname, true);
    xhr.onprogress = function() {
      this.setState({output: xhr.responseText});
    }.bind(this);
    xhr.onload = function() {
        setTimeout(function() {
            location.reload();
        }, 2000);
    }
    xhr.send(formData);
  },
  preventDefault: function(e) {
    e.preventDefault();
    e.stopPropagation();
  },
  componentDidMount: function() {
    var body = document.getElementsByTagName('body')[0];
    body.addEventListener('drop', this.handleDrop);
    body.addEventListener('dragover', this.preventDefault);
  },
  render: function() {
    return (
      <div className='deploy-popin'>
        <div className='modal-header'>
            <h3 id='myModalLabel'>New deploy</h3>
        </div>
        <div className='modal-body'>
            {this.state.deploy ? '' : <DeployBox addFile={this.addFile} />}
            {this.state.files.length > 0 ? <Files files={this.state.files} /> : ''}
            {this.state.output.length > 0 ? <Output message={this.state.output} /> : ''}
        </div>
        <div className='modal-footer'>
            <input type='hidden' id='filecontent' name='filecontent' />
            <CancelBtn disabled={this.state.deploy} />
            <StartDeployBtn deploy={this.deploy} />
        </div>
      </div>
    );
  }
});

var Components = {
    DeployBox: DeployBox,
    DeployPopin: DeployPopin
};

module.exports = Components;
