from app.business.campaign_service import CampaignService


def test_proposes_three_scripts():
    service = CampaignService(None)
    scripts = service.propose_scripts("Marca", "Producto", "clientes", "comprar")
    assert len(scripts) == 3
    assert all("Producto" in script for script in scripts)
