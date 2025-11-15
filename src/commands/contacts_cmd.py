from ..services.contacts_service import ContactsService

class ContactsCommand:
    def __init__(self):
        self.service = ContactsService()
    
    def add_contact(self, name, phone=None, email=None, address=None, birthday=None):
        try:
            result = self.service.add_contact(name, phone, email, address, birthday)
            return f"Contact '{name}'  successfully added! (ID: {result.id})"
        except Exception as e:
            return f"Error adding  contact: {str(e)}"
     
    def edit_contact(self, contact_id, **kwargs):
        try:
            result = self.service.edit_contact(contact_id, **kwargs)
            return f"Contact '{result.name}' successfully updated!"
        except Exception as e:
            return f"Error editing contact: {str(e)}"
    
    def delete_contact(self, contact_id):
        try:
            contact_name = self.service.get_contact(contact_id).name
            self.service.delete_contact(contact_id)
            return f"Contact '{contact_name}' successfully deleted!"
        except Exception as e:
            return f"Error deleting contact: {str(e)}"
    
    def search_contacts(self, query):
        try:
            results = self.service.search_contacts(query)
            if not results:
                return f"No contacts found for query '{query}'"
            
            output = ["Contact search results:"]
            for contact in results:
                contact_info = f"{contact.name}"
                if contact.phone:
                    contact_info += f" | Phone: {contact.phone}"
                if contact.email:
                    contact_info += f" | Email: {contact.email}"
                if contact.birthday:
                    contact_info += f" | Birthday: {contact.birthday}"
                output.append(contact_info)
            
            return "\n".join(output)
        except Exception as e:
            return f"Error during search: {str(e)}"
    
    def list_contacts(self):
        try:
            contacts = self.service.get_all_contacts()
            if not contacts:
                return "Contact list is empty"
            
            output = ["All contacts:"]
            for i, contact in enumerate(contacts, 1):
                contact_info = f"{i}. {contact.name}"
                if contact.phone:
                    contact_info += f" | Phone: {contact.phone}"
                if contact.email:
                    contact_info += f" | Email: {contact.email}"
                if contact.birthday:
                    contact_info += f" | Birthday: {contact.birthday}"
                output.append(contact_info)
            
            return "\n".join(output)
        except Exception as e:
            return f"Error getting contact list: {str(e)}"
