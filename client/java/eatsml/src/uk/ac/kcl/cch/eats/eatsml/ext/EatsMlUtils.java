/**
 * CollectionExtension.java
 * Sep 15, 2010
 */
package uk.ac.kcl.cch.eats.eatsml.ext;

import java.util.ArrayList;
import java.util.List;

import uk.ac.kcl.cch.eats.eatsml.Authority;
import uk.ac.kcl.cch.eats.eatsml.Collection;
import uk.ac.kcl.cch.eats.eatsml.Date;
import uk.ac.kcl.cch.eats.eatsml.Entities;
import uk.ac.kcl.cch.eats.eatsml.Entity;
import uk.ac.kcl.cch.eats.eatsml.EntityRelationship;
import uk.ac.kcl.cch.eats.eatsml.EntityRelationshipTypes;
import uk.ac.kcl.cch.eats.eatsml.EntityRelationshipTypes.EntityRelationshipType;
import uk.ac.kcl.cch.eats.eatsml.Existence;
import uk.ac.kcl.cch.eats.eatsml.Existences;
import uk.ac.kcl.cch.eats.eatsml.Languages;
import uk.ac.kcl.cch.eats.eatsml.NamePart;
import uk.ac.kcl.cch.eats.eatsml.NamePartTypes.NamePartType;
import uk.ac.kcl.cch.eats.eatsml.NameParts;
import uk.ac.kcl.cch.eats.eatsml.NameTypes.NameType;
import uk.ac.kcl.cch.eats.eatsml.Names;
import uk.ac.kcl.cch.eats.eatsml.Names.Name;
import uk.ac.kcl.cch.eats.eatsml.Note;
import uk.ac.kcl.cch.eats.eatsml.Scripts.Script;

/**
 * Extension of the Collection class, adds utility methods to deal with
 * Collections. It provides shortcuts to return a JAXB object or a List of JAXB
 * objects that require particular traversal of the Collection hierarchy.
 * 
 * @author jvieira jose.m.vieira@kcl.ac.uk
 * @author jnorrish jamie.norrish@kcl.ac.uk
 */
public class EatsMlUtils {

	/**
	 * Gets the user's default authority from the Collection.
	 * 
	 * @param c
	 *            the collection to get the authority from
	 * @return user's default authority or null
	 */
	public static Authority getDefaultAuthority(Collection c) {

		if (c == null) {
			return null;
		}

		for (Authority authority : c.getAuthorities().getAuthority()) {
			if (authority.isUserPreferred()) {
				return authority;
			}
		}

		return null;

	}

	/**
	 * Creates and adds an Entity to the Collection.
	 * 
	 * @param c
	 *            the Collection
	 * @param id
	 *            XML id used in XML referencing
	 * @return the created Entity or null
	 */
	public static Entity createEntity(Collection c, String id) {

		if (c == null) {
			return null;
		}

		Entities entities = c.getEntities();

		if (entities == null) {
			entities = new Entities();
			c.setEntities(entities);
		}

		Entity entity = new Entity();

		if (id != null) {
			entity.setId(id);
		}

		entities.getEntity().add(entity);

		return entity;

	}

	/**
	 * Creates a new ExistenceAssertion for the given Entity.
	 * 
	 * @param entity
	 *            the Entity
	 * @param authority
	 *            the Authority
	 * @return Existence or null
	 */
	public static Existence createExistence(Entity entity, Authority authority) {

		if (entity == null || authority == null) {
			return null;
		}

		Existences assertions = entity.getExistences();

		if (assertions == null) {
			assertions = new Existences();
			entity.setExistences(assertions);
		}

		Existence existence = new Existence();
		existence.setAuthority(authority);
		assertions.getExistence().add(existence);
		return existence;

	}

	/**
	 * Creates a new EntityType assertion.
	 * 
	 * @param entity
	 *            the Entity
	 * @param authority
	 *            the Authority
	 * @param et
	 *            the EntityType
	 * @param id
	 *            XML id
	 * @param isPreferred
	 *            whether it's a preferred EntityTypeAssertion
	 * @return EntityType or null
	 */
	public static Entity.EntityTypes.EntityType createEntityType(Entity entity,
			Authority authority, uk.ac.kcl.cch.eats.eatsml.Collection.EntityTypes.EntityType et) {

		if (entity == null || authority == null || et == null) {
			return null;
		}

		Entity.EntityTypes assertions = entity.getEntityTypes();

		if (assertions == null) {
			assertions = new Entity.EntityTypes();
			entity.setEntityTypes(assertions);
		}

		Entity.EntityTypes.EntityType eta = new Entity.EntityTypes.EntityType();
		eta.setEntityType(et);
		eta.setAuthority(authority);

		assertions.getEntityType().add(eta);

		return eta;

	}

	/**
	 * Creates a new NameAssertion.
	 * 
	 * @param entity
	 *            the Entity
	 * @param authority
	 *            the Authority
	 * @param nt
	 *            the NameType
	 * @param id
	 *            XML id
	 * @param isPreferred
	 *            whether it's a preferred NameAssertion
	 * @return
	 */
	public static Name createName(Entity entity,
			Authority authority, NameType nt, String id, boolean isPreferred) {

		if (entity == null || authority == null || nt == null) {
			return null;
		}

		Names names = entity.getNames();

		if (names == null) {
			names = new Names();
			entity.setNames(names);
		}

		Name name = new Name();
		name.setNameType(nt);
		name.setAuthority(authority);
		name.setIsPreferred(isPreferred);

		names.getName().add(name);

		return name;

	}

	/**
	 * Creates a NamePart.
	 * 
	 * @param na
	 *            the NameAssertion
	 * @param npt
	 *            the NamePartType
	 * @param name
	 *            the name
	 * @return NamePart or null
	 */
	public static NamePart createNamePart(Name name, NamePartType npt,
			String namePart, Languages.Language language, Script script) {

		if (name == null || npt == null || namePart == null || namePart.length() < 1) {
			return null;
		}

		NameParts parts = name.getNameParts();

		if (parts == null) {
			parts = new NameParts();
			name.setNameParts(parts);
		}

		NamePart part = new NamePart();
		part.setNamePartType(npt);
		part.setContent(namePart);
		
		if (language == null) {
			language = (Languages.Language) name.getLanguage();
		}
		if (script == null) {
			script = (Script) name.getScript();
		}
		part.setLanguage(language);
		part.setScript(script);

		parts.getNamePart().add(part);

		return part;

	}

	/**
	 * Returns a list of an entity's entity types that are associated with an authority.
	 * 
	 * @param entity
	 *            the Entity
	 * @param authority
	 *            the Authority
	 * @return List<Collection.EntityTypes.EntityType> or null
	 */
	public static List<Collection.EntityTypes.EntityType> getAuthorityEntityTypes(
			Entity entity, Authority authority) {
		if (entity == null || authority == null) {
			return null;
		}
		
		Entity.EntityTypes entityTypes = entity.getEntityTypes(); 

		if (entityTypes == null) {
			return null;
		}
		
		String authorityId = authority.getEatsId();

		List<Collection.EntityTypes.EntityType> list = new ArrayList<Collection.EntityTypes.EntityType>();
		for (Entity.EntityTypes.EntityType et : entityTypes.getEntityType()) {
			String etAuthorityId = ((Authority) et.getAuthority()).getEatsId();
			if (authorityId.equals(etAuthorityId)) {
				list.add((Collection.EntityTypes.EntityType) et.getEntityType());
			}
		}
		if (list.isEmpty()) {
			list = null;
		}
		return list;
	}

	/**
	 * Gets a list of user preferred name assertions.
	 * 
	 * @param entity
	 *            the Entity
	 * @return List<Name> or null
	 */
	public static List<Name> getDefaultNames(Entity entity) {

		if (entity == null) {
			return null;
		}

		Names names = entity.getNames();
		
		if (names == null) {
			return null;
		}

		List<Name> list = new ArrayList<Name>();

		for (Name name : names.getName()) {
			if (name.isIsPreferred()) {
				list.add(name);
			}
		}

		if (list.isEmpty()) {
			list = null;
		}

		return list;

	}

	/**
	 * Returns a list with all the dates associated with the entity's existences.
	 * 
	 * @param entity
	 *            the entity
	 * @return List<Date> or null
	 */
	public static List<Date> getExistencesDates(Entity entity) {

		if (entity == null) {
			return null;
		}
		
		Existences existences = entity.getExistences();

		if (existences == null) {
			return null;
		}

		List<Date> list = new ArrayList<Date>();

		for (Existence existence : existences.getExistence()) {
			if (existence.getDates() != null) {
				for (Date d : existence.getDates().getDate()) {
					list.add(d);
				}
			}
		}

		return list;

	}

	/**
	 * Gets a list of the entity note assertions that are external or internal
	 * to authorities that the user can edit.
	 * 
	 * @param authority
	 *            the authority
	 * @param entity
	 *            the entity
	 * @return List<Note> or null
	 */
	public static List<Note> getNotes(
			Authority authority, Entity entity) {

		if (authority == null || entity == null) {
			return null;
		}

		if (entity.getNotes() == null) {
			return null;
		}

		List<Note> list = new ArrayList<Note>();

		for (Note note : entity.getNotes().getNote()) {
			list.add(note);
		}

		return list;

	}

	/**
	 * Gets a string describing the entity relationship assertion.
	 * 
	 * @param c
	 *            the collection
	 * @param entity
	 *            the entity carrying the entity relationship assertion
	 * @param er
	 *            the entity relationship assertion
	 * @return String or null
	 */
	public static String getRelationshipText(Collection c,
			Entity entity, EntityRelationship er) {

		if (c == null || entity == null || er == null) {
			return null;
		}
		
		String domainEntityId = ((Entity) er.getDomainEntity()).getId();
		Entity otherEntity;
		EntityRelationshipType ert = (EntityRelationshipType) er.getEntityRelationshipType();
		String relationship;
		
		if (domainEntityId == entity.getId()) {
			String rangeEntityId = ((Entity) er.getRangeEntity()).getId();
			otherEntity = getEntityById(c, rangeEntityId);
			relationship = ert.getName();
		} else {
			otherEntity = getEntityById(c, domainEntityId);
			relationship = ert.getReverseName();
		}

		if (otherEntity == null) {
			return null;
		}
		
		String otherEntityName = getPreferredName(otherEntity).getAssembledForm();
		return relationship + " " + otherEntityName;

	}

	/**
	 * Gets an entity from the collection that has the given id.
	 * 
	 * @param c
	 *            the collection
	 * @param id
	 *            the entity id
	 * @return Entity or null
	 */
	public static Entity getEntityById(Collection c, String id) {

		if (c == null || id == null) {
			return null;
		}

		Entities entities = c.getEntities();

		if (entities == null) {
			return null;
		}

		for (Entity e : entities.getEntity()) {
			if (e.getId().equals(id)) {
				return e;
			}
		}

		return null;

	}
	
	/**
	 * Gets the entity relationship type from the collection that has the given
	 * id.
	 * 
	 * @param c
	 *            the collection
	 * @param id
	 *            the entity relationship id
	 * @return EntityRelationshipType or null
	 */
	public static EntityRelationshipType getEntityRelationshipTypeById(
			Collection c, String id) {

		if (c == null || id == null) {
			return null;
		}

		EntityRelationshipTypes types = c.getEntityRelationshipTypes();

		if (types == null) {
			return null;
		}

		for (EntityRelationshipType ert : types.getEntityRelationshipType()) {
			if (ert.getId().equals(id)) {
				return ert;
			}
		}

		return null;

	}

	/**
	 * Gets the preferred name for the entity.
	 * 
	 * @param entity
	 *            the entity
	 * @return Name or null
	 */
	public static Name getPreferredName(Entity entity) {

		if (entity == null) {
			return null;
		}

		List<Name> list = getDefaultNames(entity);

		if (list == null) {
			return null;
		}

		if (list.size() > 0) {
			return list.get(0);
		}

		return null;
	}

}
