
# coding: utf-8

# In[2]:


from datetime import datetime


# In[9]:


class TweetObject:
    def __init__(self,identifier,time,list_of_keywords):
            self.identifier=identifier
            self.time =time
            self.list_of_keywords=list_of_keywords
            
class CentroidObject:
    
    def __init__(self,cluster_label,start_time,last_updated_time,list_of_keywords):
            self.cluster_label=cluster_label
            self.start_time=start_time
            self.last_updated_time=last_updated_time
            self.list_of_keywords={}
            for i in list_of_keywords:
                self.list_of_keywords[i]=1
            self.buffer=[]
            self.childArray=[]
            self.parentTopic=None
            self.height=0
    
    def centroidDetails(self):
        print("cluster number",self.cluster_label)
        print("last_updated_time",self.last_updated_time)
        numberOfKeywords=0
        l=[]
        for i in self.list_of_keywords:
                l.append(i)
        print("list_of_keys",l)
        print("no of keys",len(l))
        print("no of tweets ",len(self.buffer))
        
    def clusterTopic(self):
        maxc=0
        topic=[]
        for words in self.list_of_keywords:
            if(self.list_of_keywords.get(words)>maxc):
                maxc = self.list_of_keywords.get(words)
              
                topic.append(words)
        
        print( "topic is:",topic)
        
def makeTweetObjects(list_of_keywords):
    time=0
#     time = datetime.datetime.now()
    tweet = TweetObject(0,time,list_of_keywords)
    return tweet 


def similarityBetweenTweetObjectAndClusterCentroid(cluster_object,tweet):
    cluster_centroid_list_of_keywords=cluster_object.list_of_keywords
    fading_time=1#fadingFunction(cluster_object,tweet) 
    #print(fading_time)
    #print("keywors in cluster ",cluster_centroid_list_of_keywords)
    #print("cluster,no",cluster_object.cluster_label)
   
    similar_keywords=list(set(cluster_centroid_list_of_keywords)&set(tweet.list_of_keywords))
    #print("similar",similar_keywords)
    total_keywords=list(set(cluster_centroid_list_of_keywords)|(set(tweet.list_of_keywords)))
    #total_keywords=list(set(cluster_centroid_list_of_keywords).union (set(tweet.list_of_keywords)))
    len_of_total_keywords=len(total_keywords)
    #print("total keys in cluster :",len_of_total_keywords)
    len_of_similar_keywords=len(similar_keywords)
    
    similarity=((len_of_similar_keywords/len_of_total_keywords))
    return similarity

def assignTweetObjectToClusterCentroid(centroidObj,tweetObj):
    list_of_segments_in_tweet = tweetObj.list_of_keywords
    list_of_segments_in_centroid = centroidObj.list_of_keywords
#     print(list_of_segments_in_tweet)
#     print(list_of_segments_in_centroid)
    for segment in list_of_segments_in_tweet:
        if(segment in list_of_segments_in_centroid):
            centroidObj.list_of_keywords.get(segment)
            centroidObj.list_of_keywords[segment] += 1
        else :
            centroidObj.list_of_keywords[segment] = 1
    centroidObj.buffer.append(tweetObj)
    centroidObj.last_updated_time = tweetObj.time
def activeCluster(list_of_clusters,params):
    list_of_active_clusters=[]
    for centroids in list_of_clusters:
        if(len(centroids.buffer)>=params):
            list_of_active_clusters.append(centroids)
    return list_of_active_clusters


# In[2]:


def give_list_of_active_clusters(list_of_tweet,param_for_cluster_similarity_limit,param_for_active_cluster_pruning):
    list_of_centroids=[]
    cluster_number=2
    for tweet in list_of_tweet:
        if(len(tweet.list_of_keywords)==0):
            print("Noise Tweet")
        elif(len(list_of_centroids)==0):
            time = 0
            #time = datetime.datetime.now()
            centroid=CentroidObject(1,time,time,tweet.list_of_keywords)
            centroid.buffer.append(tweet)
            list_of_centroids.append(centroid)
        else:
            maxc=-1
            most_similar_centroid=type(CentroidObject)
            for centroid in list_of_centroids:
                value=similarityBetweenTweetObjectAndClusterCentroid(centroid,tweet)
                #print(value)
                if(value>maxc):
                    maxc=value
                    most_similar_centroid=centroid
            if(maxc>=param_for_cluster_similarity_limit):
                #print(most_similar_centroid.list_of_keywords)
                assignTweetObjectToClusterCentroid(most_similar_centroid,tweet)
            else:
                centroid=CentroidObject(cluster_number,0,0,tweet.list_of_keywords)
                list_of_centroids.append(centroid)
                cluster_number+=1
    list_of_active_clusters=activeCluster(list_of_centroids,param_for_active_cluster_pruning)
    return list_of_active_clusters
#                 print("list of keys :",tweet.list_of_keywords)
#                 print("creating a new cluster ",centroid.list_of_keywords)
#                 print("created cluster no",cluster_number)


# In[12]:


def fadingFunction(centroidObj,tweetObj):
    lamda = 0.05
    time_centroid = centroidObj.last_updated_time 
    time_tweet = tweetObj.time
    #diff_new = time_tweet- timedelta(hours=time_tweet.hour,minutes=time_tweet.minute)
    print("c",time_centroid)
    print("t",time_tweet)
    diff = (time_tweet - time_centroid).seconds
    print(diff)
    return int(2**((-1)*lamda*diff))
    


# In[13]:


def similarityBetweenCentroids(centroidOne,centroidTwo):
    if centroidOne.cluster_label == centroidTwo.cluster_label:
        return 1
    else : 
        similar_keywords=list(set(centroidOne.list_of_keywords)&set(centroidTwo.list_of_keywords))
    #     print("similar",similar_keywords)
        total_keywords=list(set(centroidOne.list_of_keywords)|(set(centroidTwo.list_of_keywords)))
        len_of_similar_keywords=len(similar_keywords)
        len_of_total_keywords=len(total_keywords)
        similarity=((len_of_similar_keywords/len_of_total_keywords))
        return similarity
    
    
def intraClusterSimilarity(list_of_tweets):
    cluster_value = 0
    for tweet in list_of_tweets:
        tweet_value = 0 
        comparewithlist = list_of_tweets
        for compare_with_tweet in comparewithlist :
            if compare_with_tweet !=tweet :
                similar_keywords=list(set(tweet.list_of_keywords)&set(compare_with_tweet.list_of_keywords))
                total_keywords=list(set(tweet.list_of_keywords)|(set(compare_with_tweet.list_of_keywords)))
                len_of_similar_keywords=len(similar_keywords)
                len_of_total_keywords=len(total_keywords)
                similarity=((len_of_similar_keywords/len_of_total_keywords))
                tweet_value = tweet_value + similarity
        cluster_value=cluster_value + tweet_value
    return cluster_value
      
# In[10]:


def mergeClusters(mergeIn_cluster,merge_cluster,parent_cluster):
    if any(centroidChild == merge_cluster for centroidChild in mergeIn_cluster.childArray):
        centroidOne.childArray.remove(centroidTwo)
    elif any(centroidChild == merge_cluster for centroidChild in parent_cluster.childArray) and any(centroidChild == mergeIn_cluster for centroidChild in parent_cluster.childArray):
        list_of_keywords=list(set(mergeIn_cluster._list_of_keywords)|(set(merge_cluster.list_of_keywords)))
        buffer_elements = mergeIn_cluster + merge_cluster
        childArray = mergeIn_cluster.childArray+ merge_cluster.childArray
        parent_cluster.remove(mergeIn_cluster)
        parent_cluster.remove(merge_cluster)
        time = datetime.datetime.now()
        merged_cluster =CentroidObject(mergeIn_cluster.label,time,time,list_of_keywords)
        merged_cluster.buffer = buffer_elements
        merged_cluster.childArray = childArray
        parent_cluster.childArray.append(merged_cluster)
    else :
        print("Cannot be merged")
        
        
    
        


# In[5]:


def addChildCluster(parent_cluster,child_cluster):
    parent_cluster.childArray.append(child_cluster)
    child_cluster.parentTopic=parent_cluster.cluster_label                                 
    child_cluster.height=parent_cluster.height+1 
    


# In[7]:


def giveDetails(list_of_cluster):
    global_value = 0
    for b in list_of_cluster:
        b.clusterTopic()
        cluster_value = 0 
        cluster_value = intraClusterSimilarity(b.buffer)
        global_value = global_value + cluster_value
        print("--------------------------")
        print("cluster_value",cluster_value)
    try:
        print("Global measure for similarity among clusters : ",global_value/len(list_of_cluster))
    except:
        pass
