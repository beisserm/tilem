'''
Example 3 is identical to ex1_main.py but demonstrates how to do 
the same thing with use pubsub version 3 in "basic" mode. 

The main constraints are:
- topic message data is sent only via keyword arguments in a 
  sendMessage(). Sending more data is easy compared to pubsub 
  version 1.
- each topic along a topic branch gets only the data specific to it; 
  a subtopic must support all of its parent's data. This is 
  similar to the OO paradigm: "derived" topics "inherit" message data from
  "base" topics. 
- the first listener to subscribe to a topic is used to establish the  
  Topic Message Data Specification (TMDS) of the topic, i.e. the set 
  of keyword arguments that will be allowed/required in a sendMessage()
  for given topic.
- all subsequent listeners to subscribe to same topic must follow
  same protocol. E.g. below, first listener is listener1, sets TMDS to be
  msg (required) and extra (optional), so second on to subscribe, i.e. 
  listener2.onTopic1, must have same. 
'''

from pubsub import pub

# ------------ create some listeners --------------

def listener1(msg, extra=None):
    print 'Function listener1 received', msg

class Listener:    
    def onTopic1(self, msg, extra=None):
        print 'Method Listener.onTopic1 received', `msg`
    def onTopic2(self, msg):
        print 'Method Listener.onTopic2 received', `msg`
    def __call__(self):
        print 'Listener() called'

# ------------ register listeners ------------------

pub.subscribe(listener1, 'topic1')

listener2 = Listener()
pub.subscribe(listener2, pub.ALL_TOPICS)
pub.subscribe(listener2.onTopic1, 'topic1')
pub.subscribe(listener2.onTopic2, 'topic2')

# ------------ create a couple of senders --------------

def doSomething1():
    print '--- SENDING topic1 message ---'
    pub.sendMessage('topic1', msg='message1', extra='extra')
    print '---- SENT topic1 message ----'
    
def doSomething2():
    print '--- SENDING topic2 message ---'
    pub.sendMessage('topic2', msg=123)
    print '---- SENT topic2 message ----'
    
# --------- define the main part of application --------

def run():
    '''Loop until we get a quit message or user breaks.'''
    doSomething1()
    doSomething2()
    
    from pubsub.utils import printTreeDocs
    print 'done\nTopic tree TMDS:'
    printTreeDocs(extra="a")
    print '\nTopic tree listeners:'
    printTreeDocs(extra="L")


if __name__ == '__main__':
    run()
    