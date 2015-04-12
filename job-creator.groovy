listView('1and1') {
  description('All jobs from organization 1and1')
  jobs {
    regex('1and1-.*')
  }
  columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
  }
}
def projectNames = [
  '1and1/bill-of-materials-maven-plugin',
  '1and1/testlink-junit',
  '1and1/foss-parent',
  '1and1/ono-artifactory-shared',
  'mfriedenhagen/logstash-logback-encoder'
]

def gitURL = 'git://github.com/'
def gitWEB = 'https://github.com/'
projectNames.each {projectName ->
  mavenJob(projectName.replace('/', '-')) {
      jdk('JDK 8')
      logRotator(-1, 10, -1)
      scm {
        git {
          remote {
              url(gitURL + projectName + '.git')
          }
          configure {node ->
            node / browser(class: "hudson.plugins.git.browser.GithubWeb") {
              url(gitWEB + projectName + '.git')
            }
          }
          branch('origin/master')
          clean()
          createTag(false)
        }
      }
      triggers {
          scm('*/15 * * * *')
          cron('@daily')
      }
      mavenInstallation('Maven')
      goals('--errors --show-version clean verify')
      archivingDisabled(true)
      runHeadless(true)
      wrappers {
        mavenRelease {
          releaseGoals('-Dresume=false -DpreparationGoals=validate -DpushChanges=false -DlocalCheckout=true -Darguments="-Dgpg.skip=true -DaltDeploymentRepository=foo::default::file:///tmp/repo/" release:prepare release:perform')
      selectAppendJenkinsUsername()
        }
        timeout {
          absolute(30)
        }
      }
      publishers {
        jacocoCodeCoverage()
        extendedEmail('mfriedenhagen@gmail.com', '$DEFAULT_SUBJECT', '$DEFAULT_CONTENT')
      }
      configure {node ->
        node / buildWrappers / 'org.jenkinsCi.plugins.projectDescriptionSetter.DescriptionSetterWrapper'() {
          charset('UTF-8')
          projectDescriptionFilename('target/jenkins-description.html')
        } 
      }
  }
}
projectNames.each {projectName ->
  mavenJob(projectName.replace('/', '-') + '-branches') {
      jdk('JDK 8')
      logRotator(-1, 10, -1)
      scm {
        git {
          remote {
              url(gitURL + projectName + '.git')
          }
          configure {node ->
            node / browser(class: "hudson.plugins.git.browser.GithubWeb") {
              url(gitWEB + projectName + '.git')
            }
          }
          branch('origin/gh-pages')
          clean()
          createTag(false)
          strategy {
            inverse()
          }
        }
      }
      triggers {
          scm('*/15 * * * *')
          cron('@daily')
      }
      mavenInstallation('Maven')
      goals('--errors --show-version clean verify')
      archivingDisabled(true)
      runHeadless(true)
      wrappers {
        timeout {
          absolute(30)
        }
      }
      publishers {
        jacocoCodeCoverage()
        extendedEmail('mfriedenhagen@gmail.com', '$DEFAULT_SUBJECT', '$DEFAULT_CONTENT')
      }
      configure {node ->
        node / buildWrappers / 'org.jenkinsCi.plugins.projectDescriptionSetter.DescriptionSetterWrapper'() {
          charset('UTF-8')
          projectDescriptionFilename('target/jenkins-description.html')
        } 
      }
  }
}