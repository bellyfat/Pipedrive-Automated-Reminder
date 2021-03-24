import functions

def main():
    pipeline_id = functions.get_pipeline_id()
    stage_id = functions.get_stage_id(pipeline_id)
    pipeline_deals = functions.get_pipeline_deals(pipeline_id)
    subscribed_deals = functions.filter_subscribed_deals(pipeline_deals, stage_id)
    almost_finished_subscriptions = functions.filter_almost_finished_subscriptions(subscribed_deals)
    

main()