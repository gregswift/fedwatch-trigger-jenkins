#!/usr/bin/python

import sys
import requests

JENKINS_URL = 'https://jenkins.example.com'

class JenkinsJobRunner(object):
  url = JENKINS_URL
  extra_params = {}

  def __init__(self, source, name, version, version_url, backend, homepage):
    self.source = source
    self.name = name
    self.version = version
    self.version_url = version_url
    self.backend = backend
    self.homepage = homepage
    if self.backend.lower() == 'github':
      self.extra_params['commit'] = self.get_github_commit()

  def set_url(self, url):
    self.url = url

  def get_info(self):
    outstring = 'source: {0}\n'.format(self.source)
    outstring += 'name: {0}\n'.format(self.name)
    outstring += 'version: {0}\n'.format(self.version)
    outstring += 'version_url: {0}\n'.format(self.version_url)
    outstring += 'backend: {0}\n'.format(self.backend)
    outstring += 'homepage: {0}\n'.format(self.homepage)
    for (param, value) in self.extra_params.iteritems():
      outstring += '{0}: {1}\n'.format(param, value)
    return outstring

  def trigger_build(self):
    job_url = u'{0}/job/{1}/build'.format(self.url, self.name)
    data = { u'parameter': [
      {
        u'name': u'version',
        u'value': self.version
      }
    ]}
    data[u'parameter'][0].update(self.extra_params)
    print data

#curl -X POST JENKINS_URL/job/JOB_NAME/build \
#  --data token=TOKEN \
#  --data-urlencode json=
  def get_github_commit(self):
    ref_url = u'{0}/repos/{1}/git/refs/tags/{2}'
    req = requests.get(ref_url.format(self.url, self.version_url, self.version)
        ).json()
    return req[u'object'][u'sha']



if __name__ == '__main__':
  args = sys.argv
  (source, name, version, version_url, backend, homepage) = args[1:7]
  jjr = JenkinsJobRunner(source, name, version, version_url, backend, homepage)
  open('/tmp/{0}-{1}'.format(name, version), 'w').write(jjr.get_info())
  jjr.trigger_build()
